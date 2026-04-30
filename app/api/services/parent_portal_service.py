"""
PILLAR 2 — EXECUTIVE
EduBoost SA — Parent Report Service (Refactored)
Uses WorkerAgent base class to enforce JudiciaryStamp gate.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.judiciary.base import ExecutiveAction, JudiciaryStampRef, WorkerAgent
from app.api.judiciary.provider_router import ProviderRouter
from app.api.models.db_models import (
    DiagnosticSession,
    Learner,
    ParentLearnerLink,
    Report,
    StudyPlan,
    SubjectMastery,
)
from app.api.services.prompt_manager import PromptManager

logger = logging.getLogger(__name__)

class ParentReportService(WorkerAgent):
    """
    Generates AI-powered progress reports for parents.
    """

    def __init__(
        self,
        session: AsyncSession,
        encryption_key: Optional[str] = None,
    ):
        super().__init__(
            agent_id="parent-report-service",
            intent="generate_parent_report",
            encryption_key=encryption_key,
        )
        self._session = session

    async def _build_action(self, **kwargs) -> ExecutiveAction:  # type: ignore[override]
        learner_pseudonym: str = kwargs["learner_pseudonym"]
        grade: int = kwargs["grade"]
        streak_days: int = kwargs["streak_days"]
        total_xp: int = kwargs["total_xp"]
        subjects_mastery: dict = kwargs["subjects_mastery"]
        gaps: list = kwargs["gaps"]

        await self._assert_consent(learner_pseudonym, self._session)

        return ExecutiveAction(
            agent_id=self.agent_id,
            intent=self.intent,
            parameters={
                "grade": grade,
                "streak_days": streak_days,
                "total_xp": total_xp,
                "subjects_mastery": subjects_mastery,
                "gaps": gaps,
            },
            claimed_rules=[
                "POPIA-S11-DATA-MIN",
                "POPIA-S13-NOTIFY",
            ],
            learner_pseudonym=learner_pseudonym,
        )

    async def _execute(
        self, action: ExecutiveAction, stamp: JudiciaryStampRef, **kwargs
    ) -> Dict[str, Any]:
        self._assert_stamped()

        # Build prompt
        system_prompt, user_prompt = await self._build_prompts(
            action.parameters["grade"],
            action.parameters["streak_days"],
            action.parameters["total_xp"],
            action.parameters["subjects_mastery"],
            action.parameters["gaps"]
        )

        # Call LLM
        router = ProviderRouter()
        raw_content = await router.complete(
            prompt=user_prompt,
            system_prompt=system_prompt,
            action_id=action.action_id,
            stamp_id=stamp.stamp_id,
        )

        report_result = {
            "action_id": action.action_id,
            "stamp_id": stamp.stamp_id,
            "learner_pseudonym": action.learner_pseudonym,
            "report_content": raw_content,
        }

        # Persist to DB
        await self._persist_report(report_result)
        return report_result

    async def _build_prompts(self, grade: int, streak: int, xp: int, mastery: dict, gaps: list) -> tuple:
        try:
            system = PromptManager.get_template("parent_report", "system")
            user_template = PromptManager.get_template("parent_report", "user")
            
            mastery_str = ", ".join([f"{k}: {v}%" for k, v in mastery.items()])
            gaps_str = ", ".join([str(g) for g in gaps]) or "none"
            
            user_prompt = user_template.format(
                grade_name=f"Grade {grade}",
                streak_days=streak,
                total_xp=xp,
                subjects_mastery_str=mastery_str,
                gaps_str=gaps_str,
            )
        except Exception:
            system = "You are an educational progress report generator for parents."
            user_prompt = f"Generate report for Grade {grade}. Streak: {streak}, XP: {xp}. Mastery: {mastery}. Gaps: {gaps}."

        return system, user_prompt

    async def _persist_report(self, result: Dict[str, Any]) -> None:
        self._session.add(
            Report(
                report_id=uuid.uuid4(),
                learner_id=uuid.UUID(str(result["learner_pseudonym"])),
                report_type="parent",
                title="Parent progress report",
                content={
                    "action_id": result["action_id"],
                    "stamp_id": result["stamp_id"],
                    "body": result["report_content"],
                },
                summary=str(result["report_content"])[:500],
                generated_by="AI",
                is_shared=True,
                shared_with_guardian=True,
            )
        )
        await self._session.commit()

class ParentPortalService:
    """Read-model service for guardian portal workflows."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _assert_link(self, learner_id: uuid.UUID, guardian_id: uuid.UUID) -> None:
        result = await self._session.execute(
            select(ParentLearnerLink).where(
                ParentLearnerLink.learner_id == learner_id,
                ParentLearnerLink.parent_id == guardian_id,
            )
        )
        if result.scalar_one_or_none() is None:
            raise ValueError("Guardian is not linked to this learner")

    async def get_learner_progress_summary(
        self, learner_id: uuid.UUID, guardian_id: uuid.UUID
    ) -> Dict[str, Any]:
        await self._assert_link(learner_id, guardian_id)
        learner = await self._session.get(Learner, learner_id)
        if learner is None:
            raise ValueError(f"Learner {learner_id} not found")
        mastery_result = await self._session.execute(
            select(SubjectMastery).where(SubjectMastery.learner_id == learner_id)
        )
        return {
            "learner_id": str(learner_id),
            "grade": learner.grade,
            "overall_mastery": learner.overall_mastery,
            "streak_days": learner.streak_days,
            "total_xp": learner.total_xp,
            "subjects": [
                {
                    "subject_code": row.subject_code,
                    "mastery_score": row.mastery_score,
                    "knowledge_gaps": row.knowledge_gaps or [],
                }
                for row in mastery_result.scalars().all()
            ],
        }

    async def get_diagnostic_trends(
        self, learner_id: uuid.UUID, guardian_id: uuid.UUID, days: int = 30
    ) -> Dict[str, Any]:
        await self._assert_link(learner_id, guardian_id)
        result = await self._session.execute(
            select(DiagnosticSession)
            .where(DiagnosticSession.learner_id == learner_id)
            .order_by(DiagnosticSession.started_at.desc())
            .limit(days)
        )
        return {
            "learner_id": str(learner_id),
            "sessions": [
                {
                    "session_id": str(row.session_id),
                    "subject_code": row.subject_code,
                    "mastery_score": row.final_mastery_score,
                    "items_administered": row.items_administered,
                    "items_correct": row.items_correct,
                    "completed_at": row.completed_at.isoformat()
                    if row.completed_at
                    else None,
                }
                for row in result.scalars().all()
            ],
        }

    async def get_study_plan_adherence(
        self, learner_id: uuid.UUID, guardian_id: uuid.UUID
    ) -> Dict[str, Any]:
        await self._assert_link(learner_id, guardian_id)
        result = await self._session.execute(
            select(StudyPlan)
            .where(StudyPlan.learner_id == learner_id)
            .order_by(StudyPlan.created_at.desc())
            .limit(1)
        )
        plan = result.scalar_one_or_none()
        return {
            "learner_id": str(learner_id),
            "has_current_plan": plan is not None,
            "plan_id": str(plan.plan_id) if plan else None,
            "week_focus": plan.week_focus if plan else None,
        }

    async def generate_parent_report(
        self, learner_id: uuid.UUID, guardian_id: uuid.UUID
    ) -> Dict[str, Any]:
        progress = await self.get_learner_progress_summary(learner_id, guardian_id)
        service = ParentReportService(self._session)
        return await service.run(
            learner_pseudonym=str(learner_id),
            grade=progress["grade"],
            streak_days=progress["streak_days"],
            total_xp=progress["total_xp"],
            subjects_mastery={
                row["subject_code"]: row["mastery_score"]
                for row in progress["subjects"]
            },
            gaps=[
                gap for row in progress["subjects"] for gap in row["knowledge_gaps"]
            ],
        )

    async def export_data(
        self, learner_id: uuid.UUID, guardian_id: uuid.UUID
    ) -> Dict[str, Any]:
        from app.api.services.popia_deletion_service import PopiaDeletionService

        return await PopiaDeletionService(self._session).export_data(
            learner_id, guardian_id
        )

# Procedural wrapper
async def generate_parent_report(
    session: AsyncSession,
    learner_id: str,
    grade: int,
    streak_days: int,
    total_xp: int,
    subjects_mastery: dict,
    gaps: list
) -> Dict[str, Any]:
    service = ParentReportService(session)
    return await service.run(
        learner_pseudonym=learner_id,
        grade=grade,
        streak_days=streak_days,
        total_xp=total_xp,
        subjects_mastery=subjects_mastery,
        gaps=gaps
    )
