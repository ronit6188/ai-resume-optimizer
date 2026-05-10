"""Resume analysis using the advanced analyzer engine."""

from __future__ import annotations

from typing import Any

from app.utils.advanced_analyzer import analyze_resume as advanced_analyze


def build_prompt(resume_text: str, job_description_text: str | None = None) -> str:
    """Build prompt for analysis."""
    return (
        "Resume:\n"
        f"{resume_text}\n\n"
        "Job description:\n"
        f"{job_description_text or ''}"
    )


async def ask(prompt: str) -> dict[str, Any]:
    """Process analysis request using advanced analyzer."""
    resume_text, _, job_text = prompt.partition("Job description:\n")
    resume_text = resume_text.replace("Resume:\n", "", 1).strip()
    return analyze_resume(resume_text=resume_text, job_description_text=job_text.strip() or None)


def analyze_resume(resume_text: str, job_description_text: str | None = None) -> dict[str, Any]:
    """
    Analyze resume and generate comprehensive ATS insights.
    
    Uses the advanced analyzer engine for realistic, multi-dimensional analysis.
    """
    return advanced_analyze(resume_text, job_description_text)