"""EduBoost SA — Parent Portal Router."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, text

from app.api.core.database import AsyncSessionFactory
from app.api.routers.auth import get_current_user
from app.api.models.api_models import (
    ConsentResponse,
    ErrorResponse,
    LearnerProgressResponse,
    ParentPortalReportRequest,
    ParentReportResponse,
)
from app.api.models.db_models import ParentLearnerLink
from app.api.services.parent_portal_service import ParentPortalService
from app.api.services.popia_deletion_service import PopiaDeletionService

router = APIRouter()


async def require_guardian(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "guardian":
        raise HTTPException(
            status_code=403, detail="This endpoint requires the 'guardian' role"
        )
    return user


class ConsentRequest(BaseModel):
    learner_id: UUID
    guardian_email: str
    consent_version: int = Field(default=1, ge=1)
    consented: bool


class DeletionRequest(BaseModel):
    learner_id: UUID
    reason: Optional[str] = None


def _guardian_id(user: dict) -> UUID:
    try:
        return UUID(str(user["sub"]))
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid guardian token") from exc


async def _assert_guardian_link(session, learner_id: UUID, guardian_id: UUID) -> None:
    result = await session.execute(
        select(ParentLearnerLink).where(
            ParentLearnerLink.learner_id == learner_id,
            ParentLearnerLink.parent_id == guardian_id,
        )
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=403,
            detail="Guardian is not linked to this learner",
        )


@router.get(
    "/{learner_id}/progress/{guardian_id}", response_model=LearnerProgressResponse
)
async def get_learner_progress(
    learner_id: UUID, guardian_id: UUID, user: dict = Depends(require_guardian)
):
    """Get learner progress summary for parent portal."""
    async with AsyncSessionFactory() as session:
        try:
            token_guardian_id = _guardian_id(user)
            if token_guardian_id != guardian_id:
                raise HTTPException(status_code=403, detail="Guardian mismatch")
            service = ParentPortalService(session)
            progress = await service.get_learner_progress_summary(
                learner_id, guardian_id
            )
            return LearnerProgressResponse(success=True, progress=progress)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get progress: {e}"
            ) from e


# Backwards-compatible alias (some tests/clients use guardian-first ordering)
@router.get(
    "/{guardian_id}/progress/{learner_id}", response_model=LearnerProgressResponse
)
async def get_learner_progress_guardian_first(
    guardian_id: UUID, learner_id: UUID, user: dict = Depends(require_guardian)
):
    return await get_learner_progress(
        learner_id=learner_id, guardian_id=guardian_id, user=user
    )


@router.get("/{learner_id}/diagnostics/{guardian_id}")
async def get_diagnostic_trends(
    learner_id: UUID,
    guardian_id: UUID,
    days: int = 30,
    user: dict = Depends(require_guardian),
):
    async with AsyncSessionFactory() as session:
        try:
            token_guardian_id = _guardian_id(user)
            if token_guardian_id != guardian_id:
                raise HTTPException(status_code=403, detail="Guardian mismatch")
            service = ParentPortalService(session)
            trends = await service.get_diagnostic_trends(learner_id, guardian_id, days)
            return {"success": True, "trends": trends}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get trends: {e}"
            ) from e


@router.get("/{learner_id}/study-plan/{guardian_id}")
async def get_study_plan_adherence(
    learner_id: UUID, guardian_id: UUID, user: dict = Depends(require_guardian)
):
    async with AsyncSessionFactory() as session:
        try:
            token_guardian_id = _guardian_id(user)
            if token_guardian_id != guardian_id:
                raise HTTPException(status_code=403, detail="Guardian mismatch")
            service = ParentPortalService(session)
            adherence = await service.get_study_plan_adherence(learner_id, guardian_id)
            return {"success": True, "adherence": adherence}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get adherence: {e}"
            ) from e


@router.post(
    "/report/generate",
    status_code=status.HTTP_200_OK,
    response_model=ParentReportResponse,
)
async def generate_parent_report(
    request: ParentPortalReportRequest, user: dict = Depends(require_guardian)
):
    async with AsyncSessionFactory() as session:
        try:
            token_guardian_id = _guardian_id(user)
            if token_guardian_id != request.guardian_id:
                raise HTTPException(status_code=403, detail="Guardian mismatch")
            service = ParentPortalService(session)
            report = await service.generate_parent_report(
                learner_id=request.learner_id,
                guardian_id=request.guardian_id,
            )
            return ParentReportResponse(success=True, report=report)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=503, detail=f"Report generation failed: {e}"
            ) from e


@router.post(
    "/consent",
    status_code=status.HTTP_201_CREATED,
    response_model=ConsentResponse,
    responses={500: {"model": ErrorResponse}},
)
async def record_consent(
    request: ConsentRequest, user: dict = Depends(require_guardian)
):
    event_type = "consent_granted" if request.consented else "consent_revoked"
    async with AsyncSessionFactory() as session:
        try:
            guardian_id = _guardian_id(user)
            await _assert_guardian_link(session, request.learner_id, guardian_id)
            email_hash = (
                __import__("hashlib")
                .sha256(request.guardian_email.lower().strip().encode())
                .hexdigest()
            )
            await session.execute(
                text(
                    """
                    INSERT INTO consent_audit (pseudonym_id, event_type, consent_version, guardian_email_hash)
                    VALUES (:pid, :etype, :cv, :eh)
                    """
                ),
                {
                    "pid": str(request.learner_id),
                    "etype": event_type,
                    "cv": request.consent_version,
                    "eh": email_hash,
                },
            )
            await session.commit()
            return ConsentResponse(recorded=True, popia_compliant=True)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Consent recording failed: {e}"
            ) from e


@router.post("/deletion/request", status_code=status.HTTP_202_ACCEPTED)
async def request_deletion(
    request: DeletionRequest, user: dict = Depends(require_guardian)
):
    async with AsyncSessionFactory() as session:
        try:
            service = PopiaDeletionService(session)
            return await service.request_deletion(
                request.learner_id, _guardian_id(user), request.reason
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Deletion request failed: {e}"
            ) from e


@router.post("/deletion/execute", status_code=status.HTTP_200_OK)
async def execute_deletion(
    request: DeletionRequest, user: dict = Depends(require_guardian)
):
    async with AsyncSessionFactory() as session:
        try:
            service = PopiaDeletionService(session)
            return await service.execute_deletion(
                request.learner_id, _guardian_id(user)
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Deletion execution failed: {e}"
            ) from e


@router.get("/deletion/status/{learner_id}/{guardian_id}")
async def get_deletion_status(
    learner_id: UUID, guardian_id: UUID, user: dict = Depends(require_guardian)
):
    async with AsyncSessionFactory() as session:
        try:
            service = PopiaDeletionService(session)
            token_guardian_id = _guardian_id(user)
            if token_guardian_id != guardian_id:
                raise HTTPException(status_code=403, detail="Guardian mismatch")
            return await service.get_deletion_status(learner_id, token_guardian_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Status check failed: {e}"
            ) from e


@router.get("/export/{learner_id}/{guardian_id}")
async def export_learner_data(
    learner_id: UUID, guardian_id: UUID, user: dict = Depends(require_guardian)
):
    async with AsyncSessionFactory() as session:
        try:
            service = PopiaDeletionService(session)
            token_guardian_id = _guardian_id(user)
            if token_guardian_id != guardian_id:
                raise HTTPException(status_code=403, detail="Guardian mismatch")
            return await service.export_data(learner_id, token_guardian_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Export failed: {e}") from e


@router.get("/right-to-access/{learner_id}/{guardian_id}")
async def right_to_access(
    learner_id: UUID, guardian_id: UUID, user: dict = Depends(require_guardian)
):
    async with AsyncSessionFactory() as session:
        try:
            service = ParentPortalService(session)
            token_guardian_id = _guardian_id(user)
            if token_guardian_id != guardian_id:
                raise HTTPException(status_code=403, detail="Guardian mismatch")
            data = await service.export_data(learner_id, token_guardian_id)
            return {
                "success": True,
                "data": data,
                "metadata": {
                    "collection_date": datetime.now().isoformat(),
                    "data_subject_id": str(learner_id),
                    "popia_compliant": True,
                    "data_controller": "EduBoost SA",
                    "data_processor": "EduBoost Platform",
                },
                "instructions": "This is your complete personal data export. You have the right to request corrections or deletion.",
            }
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Right-to-access request failed: {e}"
            ) from e
