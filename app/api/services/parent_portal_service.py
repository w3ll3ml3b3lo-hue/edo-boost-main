"""
PILLAR 2 — EXECUTIVE
EduBoost SA — Parent Report Service (Refactored)
Uses WorkerAgent base class to enforce JudiciaryStamp gate.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.judiciary.base import ExecutiveAction, JudiciaryStampRef, WorkerAgent
from app.api.infrastructure.provider_router import ProviderRouter
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
        await self._session.execute(
            text(
                """
                INSERT INTO parent_reports
                    (action_id, stamp_id, learner_pseudonym, report_content, created_at)
                VALUES (:action_id, :stamp_id, :learner_pseudonym, :report_content, now())
                """
            ),
            result,
        )
        await self._session.commit()

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
