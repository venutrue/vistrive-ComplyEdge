from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    primary_contact_email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    onboarding_status: Mapped[str] = mapped_column(String(50), default="created", nullable=False)

    legal_entities: Mapped[list[LegalEntity]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    users: Mapped[list[User]] = relationship(back_populates="tenant", cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tenant: Mapped[Tenant] = relationship(back_populates="users")


class LegalEntity(Base, TimestampMixin):
    __tablename__ = "legal_entities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cin: Mapped[Optional[str]] = mapped_column(String(30))
    pan: Mapped[Optional[str]] = mapped_column(String(20))

    tenant: Mapped[Tenant] = relationship(back_populates="legal_entities")
    establishments: Mapped[list[Establishment]] = relationship(back_populates="legal_entity", cascade="all, delete-orphan")


class Establishment(Base, TimestampMixin):
    __tablename__ = "establishments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    legal_entity_id: Mapped[str] = mapped_column(
        ForeignKey("legal_entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    employee_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    legal_entity: Mapped[LegalEntity] = relationship(back_populates="establishments")
    tasks: Mapped[list[ComplianceTask]] = relationship(back_populates="establishment")
    filings: Mapped[list[Filing]] = relationship(back_populates="establishment")
    notices: Mapped[list[Notice]] = relationship(back_populates="establishment")


class Regulation(Base, TimestampMixin):
    __tablename__ = "regulations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    rules: Mapped[list[Rule]] = relationship(back_populates="regulation", cascade="all, delete-orphan")


class Rule(Base, TimestampMixin):
    __tablename__ = "rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    regulation_id: Mapped[str] = mapped_column(ForeignKey("regulations.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(100), default="ALL", nullable=False)
    min_employee_threshold: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    source_reference: Mapped[str] = mapped_column(Text, nullable=False)

    regulation: Mapped[Regulation] = relationship(back_populates="rules")
    obligations: Mapped[list[ObligationTemplate]] = relationship(back_populates="rule", cascade="all, delete-orphan")


class ObligationTemplate(Base, TimestampMixin):
    __tablename__ = "obligation_templates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id: Mapped[str] = mapped_column(ForeignKey("rules.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cadence: Mapped[str] = mapped_column(String(40), nullable=False)
    sla_days: Mapped[int] = mapped_column(Integer, default=7, nullable=False)

    rule: Mapped[Rule] = relationship(back_populates="obligations")


class ComplianceTask(Base, TimestampMixin):
    __tablename__ = "compliance_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    establishment_id: Mapped[str] = mapped_column(ForeignKey("establishments.id", ondelete="CASCADE"), nullable=False)
    obligation_template_id: Mapped[str] = mapped_column(
        ForeignKey("obligation_templates.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    applicability_reason: Mapped[str] = mapped_column(Text, nullable=False)

    establishment: Mapped[Establishment] = relationship(back_populates="tasks")


class Filing(Base, TimestampMixin):
    __tablename__ = "filings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    establishment_id: Mapped[str] = mapped_column(ForeignKey("establishments.id", ondelete="CASCADE"), nullable=False)
    form_name: Mapped[str] = mapped_column(String(255), nullable=False)
    period_label: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)

    establishment: Mapped[Establishment] = relationship(back_populates="filings")


class EvidenceDocument(Base, TimestampMixin):
    __tablename__ = "evidence_documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filing_id: Mapped[str] = mapped_column(ForeignKey("filings.id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)


class Notice(Base, TimestampMixin):
    __tablename__ = "notices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    establishment_id: Mapped[str] = mapped_column(ForeignKey("establishments.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)

    establishment: Mapped[Establishment] = relationship(back_populates="notices")


class Incident(Base, TimestampMixin):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    establishment_id: Mapped[str] = mapped_column(ForeignKey("establishments.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    channel: Mapped[str] = mapped_column(String(30), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="queued", nullable=False)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
