"""EduBoost SA — Assessments Router

Provides CRUD for the assessments catalog and handles learner attempt submission
with automatic score computation. Persists results to assessment_attempts.
"""
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import text

from app.api.core.database import AsyncSessionFactory, get_db
from app.api.models.api_models import ErrorResponse

router = APIRouter()


# ── Request / Response Schemas ─────────────────────────────────────────────────

class AttemptResponse(BaseModel):
    """A single question response within an attempt submission."""
    question_id: str
    learner_answer: str


class AttemptSubmitRequest(BaseModel):
    """Learner attempt submission payload."""
    learner_id: UUID
    responses: list[AttemptResponse]
    time_taken_seconds: int = Field(default=0, ge=0)


class AttemptResult(BaseModel):
    """Score result returned after a submitted attempt."""
    attempt_id: UUID
    assessment_id: UUID
    learner_id: UUID
    score: float                  # 0.0 – 1.0
    marks_obtained: int
    total_marks: int
    passed: bool
    time_taken_seconds: int
    correct_count: int
    incorrect_count: int
    completed_at: str


# ── Helpers ────────────────────────────────────────────────────────────────────

def _score_attempt(questions: list[dict], responses: list[AttemptResponse]) -> dict[str, Any]:
    """
    Grade a submitted attempt against the assessment questions.
    Returns marks_obtained, total_marks, score (0–1), correct/incorrect counts,
    and a per-question breakdown list.
    """
    response_map = {r.question_id: r.learner_answer.strip().lower() for r in responses}
    total_marks = 0
    marks_obtained = 0
    correct = 0
    incorrect = 0
    breakdown = []

    for q in questions:
        qid = q.get("question_id", "")
        marks = int(q.get("marks", 1))
        correct_answer = str(q.get("correct_answer", "")).strip().lower()
        learner_answer = response_map.get(qid, "").strip().lower()
        is_correct = learner_answer == correct_answer

        total_marks += marks
        if is_correct:
            marks_obtained += marks
            correct += 1
        else:
            incorrect += 1

        breakdown.append({
            "question_id": qid,
            "is_correct": is_correct,
            "marks_awarded": marks if is_correct else 0,
        })

    score = marks_obtained / total_marks if total_marks > 0 else 0.0
    return {
        "marks_obtained": marks_obtained,
        "total_marks": total_marks,
        "score": round(score, 4),
        "correct_count": correct,
        "incorrect_count": incorrect,
        "breakdown": breakdown,
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="List available assessments",
)
async def list_assessments(
    subject_code: Optional[str] = Query(default=None, description="Filter by subject (e.g. MATH, ENG)"),
    grade_level: Optional[int] = Query(default=None, ge=0, le=7),
    assessment_type: Optional[str] = Query(default=None, description="quiz | test | exam | diagnostic"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """Return paginated list of active assessments. Filterable by subject, grade, and type."""
    conditions = ["is_active = TRUE"]
    params: dict = {"limit": limit, "offset": offset}

    if subject_code:
        conditions.append("subject_code = :subject_code")
        params["subject_code"] = subject_code.upper()
    if grade_level is not None:
        conditions.append("grade_level = :grade_level")
        params["grade_level"] = grade_level
    if assessment_type:
        conditions.append("assessment_type = :assessment_type")
        params["assessment_type"] = assessment_type.lower()

    where = " AND ".join(conditions)

    async with AsyncSessionFactory() as session:
        result = await session.execute(
            text(
                f"""
                SELECT assessment_id, title, subject_code, grade_level,
                       assessment_type, total_marks, time_limit_minutes,
                       passing_score, created_at
                FROM assessments
                WHERE {where}
                ORDER BY grade_level, subject_code
                LIMIT :limit OFFSET :offset
                """
            ),
            params,
        )
        rows = [dict(r) for r in result.mappings().all()]

        count_result = await session.execute(
            text(f"SELECT COUNT(*) FROM assessments WHERE {where}"),
            {k: v for k, v in params.items() if k not in ("limit", "offset")},
        )
        total = count_result.scalar()

    return {"total": total, "offset": offset, "limit": limit, "assessments": rows}


@router.get(
    "/{assessment_id}",
    status_code=status.HTTP_200_OK,
    summary="Fetch a single assessment with its questions",
    responses={404: {"model": ErrorResponse}},
)
async def get_assessment(assessment_id: UUID):
    """Return full assessment details including the questions array."""
    async with AsyncSessionFactory() as session:
        result = await session.execute(
            text("SELECT * FROM assessments WHERE assessment_id = :id AND is_active = TRUE"),
            {"id": str(assessment_id)},
        )
        row = result.mappings().first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error="Assessment not found",
                code="ASSESSMENT_NOT_FOUND",
                details={"assessment_id": str(assessment_id)},
            ).model_dump(),
        )
    return dict(row)


@router.post(
    "/{assessment_id}/attempt",
    status_code=status.HTTP_201_CREATED,
    response_model=AttemptResult,
    summary="Submit a learner attempt and receive a score",
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def submit_attempt(
    assessment_id: UUID,
    request: AttemptSubmitRequest,
    db=Depends(get_db),
):
    """
    Score a learner's submitted attempt against the assessment answer key.
    Persists the attempt to `assessment_attempts` and returns the result.
    """
    async with AsyncSessionFactory() as session:
        # 1. Fetch assessment
        result = await session.execute(
            text("SELECT * FROM assessments WHERE assessment_id = :id AND is_active = TRUE"),
            {"id": str(assessment_id)},
        )
        row = result.mappings().first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error="Assessment not found",
                code="ASSESSMENT_NOT_FOUND",
                details={"assessment_id": str(assessment_id)},
            ).model_dump(),
        )

    assessment = dict(row)
    questions: list[dict] = assessment.get("questions") or []

    if not questions:
        raise HTTPException(
            status_code=422,
            detail=ErrorResponse(
                error="Assessment has no questions",
                code="ASSESSMENT_NO_QUESTIONS",
                details={"assessment_id": str(assessment_id)},
            ).model_dump(),
        )

    # 2. Score the attempt
    scored = _score_attempt(questions, request.responses)
    passed = scored["score"] >= float(assessment.get("passing_score", 0.5))
    completed_at = datetime.now(timezone.utc)

    # 3. Persist
    import json
    async with AsyncSessionFactory() as session:
        insert_result = await session.execute(
            text(
                """
                INSERT INTO assessment_attempts
                    (learner_id, assessment_id, score, marks_obtained,
                     time_taken_seconds, responses, completed_at)
                VALUES
                    (:learner_id, :assessment_id, :score, :marks_obtained,
                     :time_taken_seconds, :responses::jsonb, :completed_at)
                RETURNING attempt_id
                """
            ),
            {
                "learner_id": str(request.learner_id),
                "assessment_id": str(assessment_id),
                "score": scored["score"],
                "marks_obtained": scored["marks_obtained"],
                "time_taken_seconds": request.time_taken_seconds,
                "responses": json.dumps(scored["breakdown"]),
                "completed_at": completed_at,
            },
        )
        attempt_id = insert_result.scalar()
        await session.commit()

    # ── Award XP and update streak after successful attempt ──────────────
    try:
        from app.api.services.gamification_service import GamificationService
        async with AsyncSessionFactory() as session:
            service = GamificationService(session)
            xp_type = "perfect_score" if scored["score"] >= 1.0 else "diagnostic_complete"
            await service.award_xp(learner_id=request.learner_id, xp_type=xp_type)
            await service.update_streak(request.learner_id)
    except Exception:
        pass  # Best-effort: don't fail the attempt response if gamification errors

    return AttemptResult(
        attempt_id=attempt_id,
        assessment_id=assessment_id,
        learner_id=request.learner_id,
        score=scored["score"],
        marks_obtained=scored["marks_obtained"],
        total_marks=scored["total_marks"],
        passed=passed,
        time_taken_seconds=request.time_taken_seconds,
        correct_count=scored["correct_count"],
        incorrect_count=scored["incorrect_count"],
        completed_at=completed_at.isoformat(),
    )


@router.get(
    "/learner/{learner_id}/attempts",
    status_code=status.HTTP_200_OK,
    summary="List a learner's past assessment attempts",
    responses={404: {"model": ErrorResponse}},
)
async def get_learner_attempts(
    learner_id: UUID,
    subject_code: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """Return a learner's historical assessment attempts, most recent first."""
    params: dict = {
        "learner_id": str(learner_id),
        "limit": limit,
        "offset": offset,
    }
    subject_join = ""
    subject_filter = ""
    if subject_code:
        subject_join = "JOIN assessments a ON aa.assessment_id = a.assessment_id"
        subject_filter = "AND a.subject_code = :subject_code"
        params["subject_code"] = subject_code.upper()

    async with AsyncSessionFactory() as session:
        result = await session.execute(
            text(
                f"""
                SELECT aa.attempt_id, aa.assessment_id, aa.score,
                       aa.marks_obtained, aa.time_taken_seconds,
                       aa.started_at, aa.completed_at
                FROM assessment_attempts aa
                {subject_join}
                WHERE aa.learner_id = :learner_id
                {subject_filter}
                ORDER BY aa.started_at DESC
                LIMIT :limit OFFSET :offset
                """
            ),
            params,
        )
        rows = [dict(r) for r in result.mappings().all()]

        count_result = await session.execute(
            text(
                f"""
                SELECT COUNT(*) FROM assessment_attempts aa
                {subject_join}
                WHERE aa.learner_id = :learner_id {subject_filter}
                """
            ),
            {k: v for k, v in params.items() if k not in ("limit", "offset")},
        )
        total = count_result.scalar()

    return {
        "learner_id": str(learner_id),
        "total": total,
        "offset": offset,
        "limit": limit,
        "attempts": rows,
    }
