"""0001_initial_schema

[SHORT-TERM FIX 5] First Alembic migration capturing the full initial schema.

This migration replaces scripts/db_init.sql as the authoritative schema source.
All subsequent schema changes MUST be added as new Alembic revisions — never
by editing this file or the SQL init scripts directly.

Revision ID: 0001_initial
Revises:     (base)
Create Date: 2026-05-01
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# ─────────────────────────────────────────────────────────────────────────────
revision: str = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None
# ─────────────────────────────────────────────────────────────────────────────


def upgrade() -> None:
    # ── Extensions ────────────────────────────────────────────────────────────
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # ── guardians ────────────────────────────────────────────────────────────
    # Parents / guardians who grant consent for learner accounts.
    op.create_table(
        "guardians",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("email_hash", sa.Text, nullable=False, unique=True, comment="SHA-256 of normalised email — never store plaintext"),
        sa.Column("phone_hash", sa.Text, nullable=True, comment="SHA-256 of E.164 phone — never store plaintext"),
        sa.Column("display_name", sa.Text, nullable=True),
        sa.Column("password_hash", sa.Text, nullable=False),
        sa.Column("is_verified", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True, comment="Soft-delete timestamp (right-to-erasure)"),
    )
    op.create_index("ix_guardians_email_hash", "guardians", ["email_hash"])

    # ── learners ─────────────────────────────────────────────────────────────
    # Pseudonymous learner records. No PII stored here; PII lives in guardians.
    op.create_table(
        "learners",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("pseudonym_id", sa.Text, nullable=False, unique=True, comment="Opaque ID used in LLM prompts — never the real name"),
        sa.Column("guardian_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("guardians.id", ondelete="CASCADE"), nullable=False),
        sa.Column("display_name", sa.Text, nullable=True, comment="Chosen name shown in UI — not linked to real identity"),
        sa.Column("grade", sa.SmallInteger, nullable=False, comment="SA grade: 0=Grade R, 1–7=Grade 1–7"),
        sa.Column("home_language", sa.Text, nullable=True, comment="ISO 639-1 code: en, zu, af, xh ..."),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_index("ix_learners_guardian_id", "learners", ["guardian_id"])
    op.create_index("ix_learners_pseudonym_id", "learners", ["pseudonym_id"])

    # ── parental_consents ────────────────────────────────────────────────────
    op.create_table(
        "parental_consents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("guardian_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("guardians.id", ondelete="CASCADE"), nullable=False),
        sa.Column("learner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("learners.id", ondelete="CASCADE"), nullable=False),
        sa.Column("consent_version", sa.Text, nullable=False, comment="Version of the consent document accepted"),
        sa.Column("ip_address_hash", sa.Text, nullable=True, comment="Hashed IP for audit trail"),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column("consented_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("withdrawn_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("withdrawal_reason", sa.Text, nullable=True),
    )
    op.create_index("ix_consents_learner_id", "parental_consents", ["learner_id"])

    # ── diagnostic_sessions ──────────────────────────────────────────────────
    op.create_table(
        "diagnostic_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("learner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("learners.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", sa.Text, nullable=False),
        sa.Column("grade_assessed", sa.SmallInteger, nullable=False),
        sa.Column("irt_theta", sa.Float, nullable=True, comment="IRT ability estimate (theta)"),
        sa.Column("knowledge_gaps", postgresql.JSONB, nullable=True),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_index("ix_diagnostic_learner_id", "diagnostic_sessions", ["learner_id"])

    # ── study_plans ──────────────────────────────────────────────────────────
    op.create_table(
        "study_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("learner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("learners.id", ondelete="CASCADE"), nullable=False),
        sa.Column("week_start", sa.Date, nullable=False),
        sa.Column("schedule", postgresql.JSONB, nullable=False, comment="CAPS-aligned weekly schedule JSON"),
        sa.Column("generated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
    )
    op.create_index("ix_study_plans_learner_id", "study_plans", ["learner_id"])

    # ── lessons ───────────────────────────────────────────────────────────────
    op.create_table(
        "lessons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("learner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("learners.id", ondelete="SET NULL"), nullable=True),
        sa.Column("subject", sa.Text, nullable=False),
        sa.Column("grade", sa.SmallInteger, nullable=False),
        sa.Column("topic", sa.Text, nullable=False),
        sa.Column("content_json", postgresql.JSONB, nullable=False),
        sa.Column("llm_provider", sa.Text, nullable=True, comment="groq | anthropic | offline"),
        sa.Column("llm_model", sa.Text, nullable=True),
        sa.Column("generation_ms", sa.Integer, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )
    op.create_index("ix_lessons_learner_id", "lessons", ["learner_id"])

    # ── audit_events ─────────────────────────────────────────────────────────
    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True, comment="Guardian or system UUID"),
        sa.Column("actor_type", sa.Text, nullable=True, comment="guardian | system | celery"),
        sa.Column("event_type", sa.Text, nullable=False),
        sa.Column("resource_type", sa.Text, nullable=True),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("payload", postgresql.JSONB, nullable=True),
        sa.Column("ip_address_hash", sa.Text, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )
    op.create_index("ix_audit_events_actor_id", "audit_events", ["actor_id"])
    op.create_index("ix_audit_events_resource", "audit_events", ["resource_type", "resource_id"])
    op.create_index("ix_audit_events_created_at", "audit_events", ["created_at"])

    # ── deletion_requests ────────────────────────────────────────────────────
    op.create_table(
        "deletion_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("guardian_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("guardians.id"), nullable=False),
        sa.Column("learner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("learners.id"), nullable=True),
        sa.Column("scope", sa.Text, nullable=False, comment="learner | guardian | all"),
        sa.Column("reason", sa.Text, nullable=True),
        sa.Column("requested_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("scheduled_for", sa.TIMESTAMP(timezone=True), nullable=False, comment="Execution time (30-day grace period)"),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("status", sa.Text, nullable=False, server_default="'pending'", comment="pending | processing | completed | failed"),
    )
    op.create_index("ix_deletion_requests_guardian_id", "deletion_requests", ["guardian_id"])
    op.create_index("ix_deletion_requests_status", "deletion_requests", ["status"])

    # ── Trigger: auto-update updated_at ───────────────────────────────────────
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    for table in ("guardians", "learners"):
        op.execute(f"""
            CREATE TRIGGER trigger_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
        """)


def downgrade() -> None:
    for table in ("guardians", "learners"):
        op.execute(f"DROP TRIGGER IF EXISTS trigger_{table}_updated_at ON {table}")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column")

    for table in [
        "deletion_requests",
        "audit_events",
        "lessons",
        "study_plans",
        "diagnostic_sessions",
        "parental_consents",
        "learners",
        "guardians",
    ]:
        op.drop_table(table)

    op.execute('DROP EXTENSION IF EXISTS "pgcrypto"')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
