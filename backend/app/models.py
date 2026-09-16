import enum
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Float, ForeignKey, JSON, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .core.db import Base


class Role(str, enum.Enum):
    learner = "learner"
    faculty = "faculty"
    employer = "employer"
    institution = "institution"
    government = "government"
    mentor = "mentor"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="public", index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(32), default=Role.learner.value)
    locale: Mapped[str] = mapped_column(String(12), default="en")
    interests: Mapped[list] = mapped_column(JSON, default=list)
    consent_analytics: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True)
    institution_type: Mapped[str] = mapped_column(String(80))
    jurisdiction: Mapped[str] = mapped_column(String(80))
    homepage: Mapped[str] = mapped_column(String(500))
    feed_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    trust_tier: Mapped[str] = mapped_column(String(16), default="official")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class ContentItem(Base):
    __tablename__ = "content_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), index=True)
    canonical_url: Mapped[str] = mapped_column(String(1000), unique=True)
    title: Mapped[str] = mapped_column(String(500))
    abstract: Mapped[str] = mapped_column(Text, default="")
    topics: Mapped[list] = mapped_column(JSON, default=list)
    stakeholder_roles: Mapped[list] = mapped_column(JSON, default=list)
    resource_type: Mapped[str] = mapped_column(String(40), default="report")
    language: Mapped[str] = mapped_column(String(12), default="en")
    licence: Mapped[str] = mapped_column(String(80), default="link-only")
    status: Mapped[str] = mapped_column(String(24), default="pending_review", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    source: Mapped[Source] = relationship()


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    category: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text, default="")


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = (UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), index=True)
    current_level: Mapped[float] = mapped_column(Float)
    target_level: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    evidence_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    skill: Mapped[Skill] = relationship()


class LearningPlan(Base):
    __tablename__ = "learning_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(24), default="active")
    milestones: Mapped[list] = mapped_column(JSON, default=list)
    progress: Mapped[float] = mapped_column(Float, default=0)


class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    content_id: Mapped[int | None] = mapped_column(ForeignKey("content_items.id"), nullable=True)
    useful: Mapped[bool] = mapped_column(Boolean)
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

