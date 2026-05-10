"""AI Analysis service with response normalization."""

from __future__ import annotations

from typing import Any

from app.utils.advanced_analyzer import analyze_resume as advanced_analyze


class AIResponseNormalizer:
    """Normalizes AI responses to match expected schemas."""

    @staticmethod
    def normalize_keyword_matches(value: Any) -> dict | None:
        """Normalize keyword_matches to dict or None."""
        if value is None:
            return None
        if isinstance(value, dict):
            return value
        if isinstance(value, list):
            return {"matches": value, "count": len(value)}
        return {"raw": str(value)}

    @staticmethod
    def normalize_weak_sections(value: Any) -> dict | None:
        """Normalize weak_sections to dict or None."""
        if value is None:
            return None
        if isinstance(value, dict):
            return value
        if isinstance(value, list):
            return {"issues": value, "count": len(value)}
        return {"raw": str(value)}

    @staticmethod
    def normalize_score_categories(value: Any) -> list | None:
        """Normalize score_categories to list or None."""
        if value is None:
            return None

        # Handle dict format: {"Category Name": {"details": [...], "recommendations": [...], "score": 80}}
        if isinstance(value, dict):
            result = []
            for name, data in value.items():
                if isinstance(data, dict):
                    result.append({
                        "name": name,
                        "score": data.get("score", data.get("score_value", 0)),
                        "max_score": data.get("max_score", 100),
                        "details": data.get("details", []),
                        "recommendations": data.get("recommendations", []),
                    })
                else:
                    result.append({
                        "name": name,
                        "score": 0,
                        "max_score": 100,
                        "details": [],
                        "recommendations": [],
                    })
            return result if result else None

        # Handle list format
        if isinstance(value, list):
            return value

        return None

    @staticmethod
    def normalize_list_field(value: Any) -> list | None:
        """Normalize list fields."""
        if value is None:
            return None
        if isinstance(value, list):
            return value
        return [value] if value else None

    @staticmethod
    def normalize_dict_field(value: Any) -> dict | None:
        """Normalize dict fields."""
        if value is None:
            return None
        if isinstance(value, dict):
            return value
        return {"value": str(value)}

    def normalize(self, raw_result: dict[str, Any]) -> dict[str, Any]:
        """Normalize complete AI response."""
        return {
            "overall_score": raw_result.get("overall_score"),
            "seniority_classification": raw_result.get("seniority_classification"),
            "score_categories": self.normalize_score_categories(raw_result.get("score_categories")),
            "keyword_analysis": self.normalize_dict_field(raw_result.get("keyword_analysis")),
            "keyword_matches": self.normalize_keyword_matches(
                raw_result.get("keyword_analysis", {}).get("exact_matches")
            ),
            "missing_keywords": self.normalize_list_field(raw_result.get("missing_keywords")),
            "resume_structure": self.normalize_dict_field(raw_result.get("resume_structure")),
            "weak_sections": self.normalize_weak_sections(
                raw_result.get("resume_structure", {}).get("formatting_issues")
            ),
            "experience_quality": self.normalize_dict_field(raw_result.get("experience_quality")),
            "technical_analysis": self.normalize_dict_field(raw_result.get("technical_analysis")),
            "writing_quality": self.normalize_dict_field(raw_result.get("writing_quality")),
            "job_analysis": self.normalize_dict_field(raw_result.get("job_analysis")),
            "recruiter_simulation": self.normalize_dict_field(raw_result.get("recruiter_simulation")),
            "missing_skills": self.normalize_dict_field(raw_result.get("missing_skills")),
            "career_guidance": self.normalize_dict_field(raw_result.get("career_guidance")),
            "improved_bullets": self.normalize_list_field(raw_result.get("improved_bullets")),
            "suggestions": self._extract_suggestions(raw_result),
            "rewritten_bullets": self._extract_rewritten_bullets(raw_result),
            "analysis_timestamp": raw_result.get("analysis_timestamp"),
        }

    def _extract_suggestions(self, raw_result: dict) -> list:
        """Extract suggestions from score_categories."""
        score_categories = raw_result.get("score_categories")
        if isinstance(score_categories, list) and score_categories:
            first = score_categories[0]
            if isinstance(first, dict):
                return first.get("recommendations", [])
        if isinstance(score_categories, dict):
            return score_categories.get("recommendations", [])
        return []

    def _extract_rewritten_bullets(self, raw_result: dict) -> list:
        """Extract rewritten bullets."""
        bullets = raw_result.get("improved_bullets", [])
        if not bullets:
            return []
        if isinstance(bullets, list):
            return [b.get("improved") for b in bullets if isinstance(b, dict) and b.get("improved")]
        return []


class AIAnalysisEngine:
    """Engine for AI resume analysis."""

    def __init__(self):
        self.normalizer = AIResponseNormalizer()

    def analyze(
        self,
        resume_text: str,
        job_description_text: str | None = None,
    ) -> dict[str, Any]:
        """Analyze resume and return normalized response."""
        try:
            raw_result = advanced_analyze(resume_text, job_description_text)

            if not raw_result:
                return self._empty_result()

            normalized = self.normalizer.normalize(raw_result)
            return normalized
        except Exception as e:
            return self._error_result(str(e))

    def _empty_result(self) -> dict[str, Any]:
        """Return empty result structure."""
        return {
            "overall_score": None,
            "seniority_classification": None,
            "score_categories": None,
            "keyword_analysis": None,
            "keyword_matches": None,
            "missing_keywords": [],
            "resume_structure": None,
            "weak_sections": None,
            "experience_quality": None,
            "technical_analysis": None,
            "writing_quality": None,
            "job_analysis": None,
            "recruiter_simulation": None,
            "missing_skills": None,
            "career_guidance": None,
            "improved_bullets": None,
            "suggestions": [],
            "rewritten_bullets": [],
            "analysis_timestamp": None,
        }

    def _error_result(self, error: str) -> dict[str, Any]:
        """Return error result."""
        result = self._empty_result()
        result["_error"] = error
        return result