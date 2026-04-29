"""
PILLAR 2 — EXECUTIVE
EduBoost SA — Study Plan Service (Refactored)
Uses WorkerAgent base class to enforce JudiciaryStamp gate.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.judiciary.base import ExecutiveAction, JudiciaryStampRef, WorkerAgent
from app.api.infrastructure.provider_router import ProviderRouter
from app.api.services.prompt_manager import PromptManager

logger = logging.getLogger(__name__)

class StudyPlanService(WorkerAgent):
    """
    Generates AI-powered weekly study plans.
    """

    def __init__(
        self,
        session: AsyncSession,
        encryption_key: Optional[str] = None,
    ):
        super().__init__(
            agent_id="study-plan-service",
            intent="generate_study_plan",
            encryption_key=encryption_key,
        )
        self._session = session

    async def _build_action(self, **kwargs) -> ExecutiveAction:  # type: ignore[override]
        learner_pseudonym: str = kwargs["learner_pseudonym"]
        grade: int = kwargs["grade"]
        knowledge_gaps: list = kwargs.get("knowledge_gaps", [])
        subjects_mastery: dict = kwargs.get("subjects_mastery", {})

        await self._assert_consent(learner_pseudonym, self._session)

        return ExecutiveAction(
            agent_id=self.agent_id,
            intent=self.intent,
            parameters={
                "grade": grade,
                "knowledge_gaps": knowledge_gaps,
                "subjects_mastery": subjects_mastery,
            },
            claimed_rules=[
                "POPIA-S11-DATA-MIN",
                "CAPS-STUDY-PLAN-ALIGNED",
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
            action.parameters["knowledge_gaps"],
            action.parameters["subjects_mastery"]
        )

        # Call LLM
        router = ProviderRouter()
        raw_content = await router.complete(
            prompt=user_prompt,
            system_prompt=system_prompt,
            action_id=action.action_id,
            stamp_id=stamp.stamp_id,
        )

        plan_id = str(uuid.uuid4())
        plan_result = {
            "plan_id": plan_id,
            "action_id": action.action_id,
            "stamp_id": stamp.stamp_id,
            "learner_pseudonym": action.learner_pseudonym,
            "grade": action.parameters["grade"],
            "schedule": raw_content,
        }

        # Persist to DB
        await self._persist_plan(plan_result)
        return plan_result

    async def _build_prompts(self, grade: int, gaps: list, mastery: dict) -> tuple:
        try:
            system = PromptManager.get_template("study_plan", "system")
            user_template = PromptManager.get_template("study_plan", "user")
            
            gaps_summary = ", ".join([str(g) for g in gaps]) or "none"
            mastery_str = ", ".join([f"{k}: {v}%" for k, v in mastery.items()])
            
            user_prompt = user_template.format(
                grade_name=f"Grade {grade}",
                gaps_summary=gaps_summary,
                subjects_mastery_str=mastery_str,
            )
        except Exception:
            system = "You are a CAPS curriculum planner."
            user_prompt = f"Create a study plan for Grade {grade}. Gaps: {gaps}. Mastery: {mastery}."

        return system, user_prompt

    async def _persist_plan(self, result: Dict[str, Any]) -> None:
        await self._session.execute(
            text(
                """
                INSERT INTO study_plans
                    (plan_id, action_id, stamp_id, learner_id, grade, schedule, created_at)
                VALUES (:plan_id, :action_id, :stamp_id, :learner_pseudonym, :grade, :schedule, now())
                """
            ),
            result,
        )
        await self._session.commit()

# Procedural wrapper
async def generate_study_plan(
    session: AsyncSession,
    learner_id: str,
    grade: int,
    knowledge_gaps: list,
    subjects_mastery: dict
) -> Dict[str, Any]:
    service = StudyPlanService(session)
    return await service.run(
        learner_pseudonym=learner_id,
        grade=grade,
        knowledge_gaps=knowledge_gaps,
        subjects_mastery=subjects_mastery
    )
