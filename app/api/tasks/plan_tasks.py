"""Celery background tasks for study plan generation and auto-linkage."""
import asyncio
from typing import Optional
from uuid import UUID

from celery.utils.log import get_task_logger

from app.api.core.celery_app import celery_app
from app.api.core.database import AsyncSessionFactory
from app.api.services.lesson_service import generate_study_plan
from sqlalchemy import text

logger = get_task_logger(__name__)


async def _refresh_study_plan(learner_id: str):
    """Async helper to generate and persist a study plan for a learner."""
    # 1. Fetch learner's current grade and gaps from the latest diagnostic session
    async with AsyncSessionFactory() as session:
        result = await session.execute(
            text("""
                SELECT grade_level, knowledge_gaps, final_mastery_score
                FROM diagnostic_sessions
                WHERE learner_id = :learner_id AND status = 'completed'
                ORDER BY completed_at DESC
                LIMIT 1
            """),
            {"learner_id": learner_id}
        )
        row = result.mappings().first()

    if not row:
        logger.warning(f"No completed diagnostic sessions found for learner {learner_id}")
        return

    grade = row["grade_level"]
    knowledge_gaps = row["knowledge_gaps"] or []
    
    # 2. Fetch subject mastery
    async with AsyncSessionFactory() as session:
        result = await session.execute(
            text("""
                SELECT subject_code, mastery_score
                FROM subject_mastery
                WHERE learner_id = :learner_id
            """),
            {"learner_id": learner_id}
        )
        mastery_rows = result.mappings().all()
    
    subjects_mastery = {r["subject_code"]: round(r["mastery_score"] * 100) for r in mastery_rows}

    # 3. Generate the plan via LLM
    plan_data = await generate_study_plan(
        grade=grade,
        knowledge_gaps=knowledge_gaps,
        subjects_mastery=subjects_mastery,
    )

    # 4. Persist the plan to DB
    import json
    async with AsyncSessionFactory() as session:
        await session.execute(
            text("""
                INSERT INTO study_plans (learner_id, target_grade, focus_areas, schedule, rationale)
                VALUES (:learner_id, :target_grade, :focus_areas, :schedule::jsonb, :rationale)
            """),
            {
                "learner_id": learner_id,
                "target_grade": grade,
                "focus_areas": json.dumps(knowledge_gaps),
                "schedule": json.dumps(plan_data.get("days", {})),
                "rationale": plan_data.get("week_focus", "Auto-generated after diagnostic."),
            }
        )
        await session.commit()
    logger.info(f"Successfully refreshed study plan for learner {learner_id}")


@celery_app.task(name="eduboost.tasks.refresh_study_plan")
def refresh_study_plan_task(learner_id_str: str) -> str:
    """
    Celery task to automatically generate a new study plan after a diagnostic session.
    """
    logger.info(f"Starting auto-linkage study plan refresh for learner: {learner_id_str}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_refresh_study_plan(learner_id_str))
    return f"Study plan generated for {learner_id_str}"
