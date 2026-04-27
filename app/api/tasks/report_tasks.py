"""Celery background tasks for automated parent report generation."""
import asyncio

from celery.utils.log import get_task_logger
from sqlalchemy import text

from app.api.core.celery_app import celery_app
from app.api.core.database import AsyncSessionFactory

logger = get_task_logger(__name__)


@celery_app.task(
    name="eduboost.tasks.weekly_parent_reports",
    bind=True,
    max_retries=2,
    default_retry_delay=120,
)
def weekly_parent_reports(self) -> str:
    """
    Beat-triggered: generate weekly parent progress reports.
    Runs every Monday at 08:00 SAST.
    """
    logger.info("Starting weekly parent report generation")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        count = loop.run_until_complete(_generate_all_reports())
        return f"Generated {count} parent reports"
    except Exception as exc:
        logger.error(f"Weekly report generation failed: {exc}")
        raise self.retry(exc=exc)
    finally:
        loop.close()


async def _generate_all_reports() -> int:
    """Generate reports for all guardians with linked learners."""
    async with AsyncSessionFactory() as session:
        result = await session.execute(
            text("""
                SELECT DISTINCT pll.parent_id::text, pll.learner_id::text
                FROM parent_learner_links pll
                JOIN learners l ON pll.learner_id = l.learner_id
                WHERE l.last_active_at >= NOW() - INTERVAL '7 days'
            """)
        )
        links = result.fetchall()

    logger.info(f"Weekly reports: {len(links)} guardian-learner pairs to process")
    generated = 0
    for parent_id, learner_id in links:
        try:
            async with AsyncSessionFactory() as session:
                from app.api.services.parent_portal_service import ParentPortalService
                import uuid
                service = ParentPortalService(session)
                await service.generate_parent_report(
                    learner_id=uuid.UUID(learner_id),
                    guardian_id=uuid.UUID(parent_id),
                )
                generated += 1
        except Exception as e:
            logger.error(f"Report generation failed for parent={parent_id} learner={learner_id}: {e}")

    return generated
