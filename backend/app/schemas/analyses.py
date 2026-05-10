"""Pydantic schemas for analysis endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AnalysisCreatePayload(BaseModel):
    resume_id: str = Field(..., description="ID of the uploaded resume to analyze")
    job_desc_id: str | None = Field(None, description="Optional job description ID for matching")


class SeniorityClassification(BaseModel):
    level: str
    confidence_score: float
    explanation: str
    strengths: list[str]
    weaknesses: list[str]
    next_level_requirements: list[str]


class ScoreCategory(BaseModel):
    name: str
    score: int
    max_score: int
    details: list[str]
    recommendations: list[str]


class KeywordAnalysis(BaseModel):
    exact_matches: list[str]
    semantic_matches: list[str]
    missing_critical: list[str]
    match_percentage: float


class ResumeStructure(BaseModel):
    has_contact_info: bool
    has_summary: bool
    has_experience: bool
    has_education: bool
    has_skills: bool
    has_projects: bool
    section_count: int
    readability_score: int
    formatting_issues: list[str]


class ExperienceQuality(BaseModel):
    measurable_achievements: list[str]
    leadership_indicators: list[str]
    project_complexity: list[str]
    impact_statements: list[str]
    quality_score: int


class TechnicalAnalysis(BaseModel):
    programming_languages: list[str]
    frameworks: list[str]
    databases: list[str]
    cloud_devops: list[str]
    ai_ml_tools: list[str]
    other_technologies: list[str]
    maturity_level: str


class WritingQuality(BaseModel):
    grammar_issues: list[str]
    weak_phrases: list[str]
    passive_voice_count: int
    repetitive_language: list[str]
    vague_descriptions: list[str]
    overall_score: int


class JobAnalysis(BaseModel):
    extracted_skills: list[str]
    seniority_requirement: str
    hidden_expectations: list[str]
    match_percentage: float
    candidate_fit: str
    missing_skills: list[str]


class RecruiterSimulation(BaseModel):
    first_impression: str
    strengths: list[str]
    red_flags: list[str]
    missing_information: list[str]
    hiring_likelihood: str
    interview_probability: str
    quick_notes: str


class MissingSkills(BaseModel):
    technologies: list[str]
    certifications: list[str]
    leadership_gaps: list[str]
    experience_gaps: list[str]
    metrics_gaps: list[str]


class CareerGuidance(BaseModel):
    roadmap_to_next_level: list[dict[str, str]]
    recommended_projects: list[dict[str, str]]
    recommended_certifications: list[str]
    suggested_technologies: list[str]
    improvement_priorities: list[dict[str, str]]


class ImprovedBullet(BaseModel):
    original: str
    improved: str
    improvement_type: str
    explanation: str


class AnalysisResponse(BaseModel):
    id: str
    resume_id: str
    job_desc_id: str | None = None
    created_at: datetime

    # Legacy fields (kept for backward compatibility)
    ats_score: int | None = None
    keyword_matches: dict | None = None
    missing_keywords: list[str] | None = None
    weak_sections: dict | None = None
    suggestions: list[str] | None = None
    rewritten_bullets: list[str] | None = None

    # New comprehensive analysis fields
    overall_score: int | None = None
    seniority_classification: SeniorityClassification | None = None
    score_categories: list[ScoreCategory] | None = None
    keyword_analysis: KeywordAnalysis | None = None
    resume_structure: ResumeStructure | None = None
    experience_quality: ExperienceQuality | None = None
    technical_analysis: TechnicalAnalysis | None = None
    writing_quality: WritingQuality | None = None
    job_analysis: JobAnalysis | None = None
    recruiter_simulation: RecruiterSimulation | None = None
    missing_skills: MissingSkills | None = None
    career_guidance: CareerGuidance | None = None
    improved_bullets: list[ImprovedBullet] | None = None
    analysis_timestamp: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('id', 'resume_id', 'job_desc_id', mode='before')
    @classmethod
    def convert_uuid(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class AnalysisListResponse(BaseModel):
    analyses: list[AnalysisResponse]

    model_config = ConfigDict(from_attributes=True)