"""SQLAlchemy model definitions with PostgreSQL support."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, LargeBinary, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True, doc="User email address")
    password_hash = Column(String(255), nullable=False, doc="Bcrypt hashed password")
    is_active = Column(Boolean, default=True, nullable=False, doc="Account active status")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False, doc="Original uploaded filename")
    uploaded_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    pdf_data = Column(LargeBinary, nullable=True, doc="PDF binary data")
    extracted_text = Column(Text, nullable=True, doc="Extracted text from PDF")

    user = relationship("User", back_populates="resumes")
    analyses = relationship("Analysis", back_populates="resume", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('user_id', 'filename', name='uq_user_filename'),
    )

    def __repr__(self):
        return f"<Resume(id={self.id}, user_id={self.user_id}, filename={self.filename})>"


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, doc="Job title")
    description_text = Column(Text, nullable=False, doc="Full job description text")
    uploaded_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="job_descriptions")
    analyses = relationship("Analysis", back_populates="job_description", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JobDescription(id={self.id}, user_id={self.user_id}, title={self.title})>"


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_desc_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)

    ats_score = Column(Integer, nullable=True, doc="ATS compatibility score 0-100")
    keyword_matches = Column(JSON, nullable=True, doc="Matched keywords from job description")
    missing_keywords = Column(JSON, nullable=True, doc="Missing keywords from job description")
    weak_sections = Column(JSON, nullable=True, doc="Weak sections identified")
    suggestions = Column(JSON, nullable=True, doc="Improvement suggestions")
    rewritten_bullets = Column(JSON, nullable=True, doc="Rewritten bullet points")

    overall_score = Column(Integer, nullable=True, doc="Overall analysis score 0-100")
    seniority_classification = Column(JSON, nullable=True, doc="Seniority level classification")
    score_categories = Column(JSON, nullable=True, doc="Score breakdown by category")
    keyword_analysis = Column(JSON, nullable=True, doc="Detailed keyword analysis")
    resume_structure = Column(JSON, nullable=True, doc="Resume structure analysis")
    experience_quality = Column(JSON, nullable=True, doc="Experience quality assessment")
    technical_analysis = Column(JSON, nullable=True, doc="Technical skills analysis")
    writing_quality = Column(JSON, nullable=True, doc="Writing quality analysis")
    job_analysis = Column(JSON, nullable=True, doc="Job description analysis")
    recruiter_simulation = Column(JSON, nullable=True, doc="Recruiter perspective simulation")
    missing_skills = Column(JSON, nullable=True, doc="Missing skills gap analysis")
    career_guidance = Column(JSON, nullable=True, doc="Career development guidance")
    improved_bullets = Column(JSON, nullable=True, doc="Improved bullet point suggestions")
    analysis_timestamp = Column(String(50), nullable=True, doc="Analysis timestamp")

    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")

    def __repr__(self):
        return f"<Analysis(id={self.id}, user_id={self.user_id}, resume_id={self.resume_id}, overall_score={self.overall_score})>"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    stripe_customer_id = Column(String(255), unique=True, nullable=False, doc="Stripe customer ID")
    plan = Column(String(50), nullable=False, doc="Subscription plan name")
    status = Column(String(50), nullable=False, doc="Subscription status")
    began_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=True, doc="Subscription end date")

    user = relationship("User", back_populates="subscriptions")

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan={self.plan}, status={self.status})>"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, doc="Action type")
    ip_address = Column(String(45), nullable=True, doc="Client IP address")
    user_agent = Column(String(500), nullable=True, doc="Client user agent")
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    details = Column(JSON, nullable=True, doc="Additional action details")

    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, user_id={self.user_id}, action={self.action}, timestamp={self.timestamp})>"