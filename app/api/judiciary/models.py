from __future__ import annotations

import hashlib
import uuid
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator
from sqlalchemy import (
    Date,
    DateTime,
    Enum as SAEnum,
    Float,
    String,
    Text,
    UniqueConstraint,
    event,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# PILLAR 1 — LEGISLATURE
# ---------------------------------------------------------------------------
class ConstitutionalRuleORM(Base):
    __tablename__ = "constitutional_rules"
    __table_args__ = (
        UniqueConstraint("rule_id", "effective_date", name="uq_rule_version"),
        {"comment": "Immutable policy rules; UPDATE/DELETE blocked by DB trigger"},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rule_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    source_document: Mapped[str] = mapped_column(String(256), nullable=False)
    rule_text: Mapped[str] = mapped_column(Text, nullable=False)
    scope_subjects: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    scope_grade_min: Mapped[Optional[int]] = mapped_column(nullable=True)
    scope_grade_max: Mapped[Optional[int]] = mapped_column(nullable=True)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    immutable_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False,
    )


@event.listens_for(ConstitutionalRuleORM, "before_update")
def _block_update(mapper, connection, target):  # noqa: ANN001
    raise RuntimeError(
        "ConstitutionalRule records are immutable. "
        "Insert a new row with a later effective_date instead."
    )


@event.listens_for(ConstitutionalRuleORM, "before_delete")
def _block_delete(mapper, connection, target):  # noqa: ANN001
    raise RuntimeError("ConstitutionalRule records cannot be deleted.")


class ScopeModel(BaseModel):
    subjects: List[str] = Field(default_factory=list)
    grade_min: int = Field(0, ge=0, le=12)
    grade_max: int = Field(12, ge=0, le=12)


class ConstitutionalRule(BaseModel):
    """Immutable policy rule with SHA-256 content hash."""

    rule_id: str = Field(..., description="Stable rule identifier, e.g. POPIA-S11-DATA-MIN")
    source_document: str = Field(..., description="Document name + version slug")
    rule_text: str = Field(..., description="Full normative text of the rule")
    scope: ScopeModel = Field(default_factory=ScopeModel)
    effective_date: date
    immutable_hash: str = Field(
        default="", description="SHA-256 of canonical fields; auto-computed if empty"
    )

    model_config = {"frozen": True}

    @model_validator(mode="after")
    def _auto_hash(self) -> "ConstitutionalRule":
        if not self.immutable_hash:
            object.__setattr__(self, "immutable_hash", self._compute_hash())
        return self

    def _compute_hash(self) -> str:
        canonical = (
            f"{self.rule_id}\x00{self.source_document}\x00"
            f"{self.rule_text}\x00{self.effective_date.isoformat()}"
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def verify_integrity(self) -> bool:
        """True if stored hash matches freshly-computed hash."""
        return self.immutable_hash == self._compute_hash()

    @classmethod
    def from_orm(cls, row: ConstitutionalRuleORM) -> "ConstitutionalRule":
        return cls(
            rule_id=row.rule_id,
            source_document=row.source_document,
            rule_text=row.rule_text,
            scope=ScopeModel(
                subjects=row.scope_subjects or [],
                grade_min=row.scope_grade_min or 0,
                grade_max=row.scope_grade_max or 12,
            ),
            effective_date=row.effective_date,
            immutable_hash=row.immutable_hash,
        )


class RuleSetSignatureORM(Base):
    """Stores operator keypair signature over the full rule bundle."""
    __tablename__ = "rule_set_signatures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bundle_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    signature: Mapped[str] = mapped_column(Text, nullable=False)
    signed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    rule_count: Mapped[int] = mapped_column(nullable=False)
    signer_key_id: Mapped[str] = mapped_column(String(128), nullable=False)


# ---------------------------------------------------------------------------
# PILLAR 3 — JUDICIARY
# ---------------------------------------------------------------------------
class StampVerdict(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ExecutiveActionIn(BaseModel):
    action_id: str
    agent_id: str
    intent: str
    parameters: Dict[str, Any] = Field(default_factory=lambda: {})
    claimed_rules: List[str] = Field(default_factory=lambda: [])
    learner_pseudonym: Optional[str] = None
    timestamp: datetime
    signature: str = ""


class JudiciaryStamp(BaseModel):
    stamp_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action_id: str
    verdict: StampVerdict
    rules_checked: List[str] = Field(default_factory=lambda: [])
    reason: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewer_model_version: str = ""


class JudiciaryStampORM(Base):
    __tablename__ = "judiciary_stamps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stamp_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True, index=True)
    action_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    verdict: Mapped[str] = mapped_column(
        SAEnum(StampVerdict, name="stamp_verdict_enum"), nullable=False
    )
    rules_checked: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    reason: Mapped[str] = mapped_column(Text, nullable=False, default="")
    reviewer_model_version: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class ConstitutionalViolationORM(Base):
    __tablename__ = "constitutional_violations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    violation_id: Mapped[str] = mapped_column(
        String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4())
    )
    action_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    stamp_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    agent_id: Mapped[str] = mapped_column(String(128), nullable=False)
    violation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    learner_pseudonym: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    audit_event_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)


# ---------------------------------------------------------------------------
# PILLAR 5 — ETHER
# ---------------------------------------------------------------------------
class Sephira(str, Enum):
    KETER = "Keter"
    CHOKHMAH = "Chokhmah"
    BINAH = "Binah"
    CHESED = "Chesed"
    GEVURAH = "Gevurah"
    TIFERET = "Tiferet"
    NETZACH = "Netzach"
    HOD = "Hod"
    YESOD = "Yesod"
    MALKUTH = "Malkuth"


class MetaphorStyle(str, Enum):
    NARRATIVE = "narrative"
    ANALYTICAL = "analytical"
    VISUAL = "visual"
    KINESTHETIC = "kinesthetic"


class NarrativeFrame(str, Enum):
    HERO = "hero"
    EXPLORER = "explorer"
    BUILDER = "builder"
    HEALER = "healer"


class LearnerEtherProfileORM(Base):
    __tablename__ = "ether_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    learner_pseudonym: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    dominant_sephira: Mapped[str] = mapped_column(String(32), nullable=False, default=Sephira.TIFERET.value)
    tone_pacing: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    metaphor_style: Mapped[str] = mapped_column(String(32), nullable=False, default=MetaphorStyle.NARRATIVE.value)
    warmth_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
    challenge_tolerance: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    preferred_narrative_frame: Mapped[str] = mapped_column(String(32), nullable=False, default=NarrativeFrame.EXPLORER.value)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), onupdate=datetime.now
    )


class LearnerEtherProfile(BaseModel):
    learner_pseudonym: str
    dominant_sephira: Sephira = Sephira.TIFERET
    tone_pacing: float = Field(0.5, ge=0.0, le=1.0)
    metaphor_style: MetaphorStyle = MetaphorStyle.NARRATIVE
    warmth_level: float = Field(0.7, ge=0.0, le=1.0)
    challenge_tolerance: float = Field(0.5, ge=0.0, le=1.0)
    preferred_narrative_frame: NarrativeFrame = NarrativeFrame.EXPLORER
    updated_at: Optional[datetime] = None
