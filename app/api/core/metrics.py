"""
EduBoost SA — Custom Prometheus Metrics

Defines application-specific counters, histograms, and gauges
for observability beyond the default HTTP instrumentation.
"""
try:
    from prometheus_client import Counter, Histogram, Gauge

    # ── Lesson Generation ──────────────────────────────────────────────────
    LESSON_GENERATION_DURATION = Histogram(
        "eduboost_lesson_generation_duration_seconds",
        "Time taken to generate a lesson via LLM",
        ["model", "grade_level", "subject"],
        buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
    )

    LESSON_GENERATION_TOTAL = Counter(
        "eduboost_lesson_generation_total",
        "Total lesson generation requests",
        ["model", "status"],  # status: success, error, fallback
    )

    # ── Diagnostic Engine ──────────────────────────────────────────────────
    DIAGNOSTIC_SESSION_TOTAL = Counter(
        "eduboost_diagnostic_session_total",
        "Total diagnostic sessions started",
        ["subject", "grade_level"],
    )

    DIAGNOSTIC_DURATION = Histogram(
        "eduboost_diagnostic_duration_seconds",
        "Time taken for a full diagnostic session",
        ["subject"],
        buckets=[10, 30, 60, 120, 300, 600],
    )

    # ── Celery Task Queue ──────────────────────────────────────────────────
    CELERY_TASK_TOTAL = Counter(
        "eduboost_celery_task_total",
        "Total Celery tasks executed",
        ["task_name", "status"],  # status: success, failure, retry
    )

    CELERY_TASK_DURATION = Histogram(
        "eduboost_celery_task_duration_seconds",
        "Celery task execution duration",
        ["task_name"],
        buckets=[1, 5, 10, 30, 60, 120, 300],
    )

    CELERY_QUEUE_DEPTH = Gauge(
        "eduboost_celery_queue_depth",
        "Number of tasks waiting in Celery queue",
        ["queue_name"],
    )

    # ── Gamification ───────────────────────────────────────────────────────
    XP_AWARDED_TOTAL = Counter(
        "eduboost_xp_awarded_total",
        "Total XP awarded to learners",
        ["xp_type"],
    )

    BADGE_AWARDED_TOTAL = Counter(
        "eduboost_badge_awarded_total",
        "Total badges awarded",
        ["badge_type"],
    )

    # ── Auth / Sessions ────────────────────────────────────────────────────
    AUTH_EVENTS_TOTAL = Counter(
        "eduboost_auth_events_total",
        "Authentication events",
        ["event_type"],  # login, register, link_learner, failed_login
    )

    ACTIVE_LEARNER_SESSIONS = Gauge(
        "eduboost_active_learner_sessions",
        "Number of active learner sessions (approximate)",
    )

    # ── API Error Rates ────────────────────────────────────────────────────
    API_ERRORS_TOTAL = Counter(
        "eduboost_api_errors_total",
        "API errors by endpoint and status code",
        ["endpoint", "status_code"],
    )

    METRICS_AVAILABLE = True

except ImportError:
    # Prometheus client not installed — provide no-op stubs
    class _NoOp:
        def labels(self, *args, **kwargs): return self
        def inc(self, *args, **kwargs): pass
        def dec(self, *args, **kwargs): pass
        def set(self, *args, **kwargs): pass
        def observe(self, *args, **kwargs): pass
        def time(self): return self
        def __enter__(self): return self
        def __exit__(self, *args): pass

    LESSON_GENERATION_DURATION = _NoOp()
    LESSON_GENERATION_TOTAL = _NoOp()
    DIAGNOSTIC_SESSION_TOTAL = _NoOp()
    DIAGNOSTIC_DURATION = _NoOp()
    CELERY_TASK_TOTAL = _NoOp()
    CELERY_TASK_DURATION = _NoOp()
    CELERY_QUEUE_DEPTH = _NoOp()
    XP_AWARDED_TOTAL = _NoOp()
    BADGE_AWARDED_TOTAL = _NoOp()
    AUTH_EVENTS_TOTAL = _NoOp()
    ACTIVE_LEARNER_SESSIONS = _NoOp()
    API_ERRORS_TOTAL = _NoOp()

    METRICS_AVAILABLE = False
