"""
EduBoost SA — Celery application with production-ready configuration.

Includes:
- Retry/dead-letter handling
- Task routing with priority queues
- Celery Beat scheduled tasks
- Task lifecycle hooks for observability
"""
from celery import Celery, signals
from celery.schedules import crontab

import structlog

from app.api.core.config import settings

log = structlog.get_logger()

celery_app = Celery(
    "eduboost",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.api.tasks.plan_tasks",
        "app.api.tasks.report_tasks",
    ],
)

# ── Core Configuration ─────────────────────────────────────────────────────────
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Johannesburg",
    enable_utc=True,

    # ── Retry & Dead-Letter ────────────────────────────────────────────────
    task_acks_late=True,                    # Acknowledge after completion
    task_reject_on_worker_lost=True,        # Requeue if worker crashes
    task_default_retry_delay=30,            # 30s between retries
    task_max_retries=3,                     # Max 3 retries
    task_time_limit=600,                    # Hard limit: 10 minutes
    task_soft_time_limit=300,               # Soft limit: 5 minutes

    # ── Priority Queues ────────────────────────────────────────────────────
    task_default_queue="default",
    task_queues={
        "critical": {"exchange": "critical", "routing_key": "critical"},
        "default": {"exchange": "default", "routing_key": "default"},
        "batch": {"exchange": "batch", "routing_key": "batch"},
    },
    task_routes={
        "eduboost.tasks.refresh_study_plan": {"queue": "critical"},
        "eduboost.tasks.generate_report": {"queue": "batch"},
        "eduboost.health.ping": {"queue": "default"},
    },

    # ── Result Backend ─────────────────────────────────────────────────────
    result_expires=3600,                    # Results expire after 1 hour

    # ── Worker Settings ────────────────────────────────────────────────────
    worker_prefetch_multiplier=1,           # Fair scheduling
    worker_concurrency=4,                   # 4 concurrent tasks per worker
)

# ── Celery Beat Schedule ───────────────────────────────────────────────────────
celery_app.conf.beat_schedule = {
    "daily-plan-refresh": {
        "task": "eduboost.tasks.daily_plan_refresh",
        "schedule": crontab(hour=5, minute=0),  # 05:00 SAST daily
        "options": {"queue": "batch"},
    },
    "weekly-parent-reports": {
        "task": "eduboost.tasks.weekly_parent_reports",
        "schedule": crontab(hour=8, minute=0, day_of_week="monday"),  # Monday 08:00 SAST
        "options": {"queue": "batch"},
    },
    "health-ping": {
        "task": "eduboost.health.ping",
        "schedule": 60.0,  # Every 60 seconds
    },
}


# ── Task Lifecycle Hooks (Observability) ───────────────────────────────────────

@signals.task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kw):
    log.info(
        "celery.task.started",
        task_name=sender.name if sender else "unknown",
        task_id=task_id,
    )


@signals.task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, retval=None, state=None, **kw):
    log.info(
        "celery.task.completed",
        task_name=sender.name if sender else "unknown",
        task_id=task_id,
        state=state,
    )


@signals.task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, **kw):
    log.error(
        "celery.task.failed",
        task_name=sender.name if sender else "unknown",
        task_id=task_id,
        error=str(exception),
    )


@signals.task_retry.connect
def task_retry_handler(sender=None, request=None, reason=None, **kw):
    log.warning(
        "celery.task.retrying",
        task_name=sender.name if sender else "unknown",
        task_id=request.id if request else "unknown",
        reason=str(reason),
    )


# ── Health Check Task ──────────────────────────────────────────────────────────

@celery_app.task(name="eduboost.health.ping")
def ping() -> str:
    return "pong"
