"""
Advanced Resume Analysis Engine
A comprehensive ATS analysis system that behaves like:
- Real ATS software
- Technical recruiter
- Hiring manager
- Career coach
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# ============== DATA DEFINITIONS ==============

SENIORITY_LEVELS = [
    "Rookie", "Beginner", "Fresher", "Junior", 
    "Intermediate", "Professional", "Senior", "Expert"
]

TECH_CATEGORIES = {
    "programming_languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "sql"
    ],
    "frameworks": [
        "react", "angular", "vue", "node", "django", "flask", "spring",
        "rails", "laravel", "nextjs", "nuxt", "svelte", "fastapi", "express"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "oracle",
        "sql server", "sqlite", "dynamodb", "cassandra", "firebase", "supabase"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
        "git", "github", "gitlab", "ci/cd", "devops", "linux", "nginx"
    ],
    "ai_ml": [
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
        "scikit-learn", "nlp", "computer vision", "pandas", "numpy", "spark",
        "hadoop", "llm", "gpt", "chatgpt", "openai", "hugging face"
    ],
    "other_tech": [
        "graphql", "rest", "api", "microservices", "agile", "scrum",
        "tailwind", "bootstrap", "sass", "webpack", "vite"
    ]
}

ACTION_VERBS = {
    "leadership": ["led", "managed", "directed", "coordinated", "oversaw", "spearheaded", "championed"],
    "technical": ["developed", "designed", "implemented", "architected", "engineered", "built", "created"],
    "achievement": ["achieved", "delivered", "improved", "optimized", "increased", "reduced", "transformed"],
    "collaboration": ["collaborated", "partnered", "worked", "cooperated", "facilitated", "negotiated"],
    "analysis": ["analyzed", "investigated", "evaluated", "assessed", "diagnosed", "audited"],
    "communication": ["presented", "communicated", "documented", "reported", "trained", "mentored"]
}

WEAK_PHRASES = [
    "worked on", "responsible for", "helped with", "assisted in", "participated in",
    "some experience", "good knowledge", "familiar with", "basic understanding",
    "occasionally", "sometimes", "occasionally"
]

PASSIVE_PHRASES = [
    "was responsible for", "was assigned to", "was given", "was provided",
    "was tasked with", "was expected to", "was required to"
]

# ============== DATA CLASSES ==============

@dataclass
class SeniorityClassification:
    level: str
    confidence_score: float
    explanation: str
    strengths: List[str]
    weaknesses: List[str]
    next_level_requirements: List[str]

@dataclass 
class ScoreCategory:
    name: str
    score: int
    max_score: int
    details: List[str]
    recommendations: List[str]

@dataclass
class KeywordAnalysis:
    exact_matches: List[str]
    semantic_matches: List[str]
    missing_critical: List[str]
    match_percentage: float

@dataclass
class ResumeStructure:
    has_contact_info: bool
    has_summary: bool
    has_experience: bool
    has_education: bool
    has_skills: bool
    has_projects: bool
    section_count: int
    readability_score: int
    formatting_issues: List[str]

@dataclass
class ExperienceQuality:
    measurable_achievements: List[str]
    leadership_indicators: List[str]
    project_complexity: List[str]
    impact_statements: List[str]
    quality_score: int

@dataclass
class TechnicalAnalysis:
    programming_languages: List[str]
    frameworks: List[str]
    databases: List[str]
    cloud_devops: List[str]
    ai_ml_tools: List[str]
    other_technologies: List[str]
    maturity_level: str

@dataclass
class WritingQuality:
    grammar_issues: List[str]
    weak_phrases: List[str]
    passive_voice_count: int
    repetitive_language: List[str]
    vague_descriptions: List[str]
    overall_score: int

@dataclass
class RecruiterSimulation:
    first_impression: str
    strengths: List[str]
    red_flags: List[str]
    missing_information: List[str]
    hiring_likelihood: str
    interview_probability: str
    quick_notes: str

@dataclass
class JobAnalysis:
    extracted_skills: List[str]
    seniority_requirement: str
    hidden_expectations: List[str]
    match_percentage: float
    candidate_fit: str
    missing_skills: List[str]

@dataclass
class MissingSkills:
    technologies: List[str]
    certifications: List[str]
    leadership_gaps: List[str]
    experience_gaps: List[str]
    metrics_gaps: List[str]

@dataclass
class CareerGuidance:
    roadmap_to_next_level: List[Dict[str, str]]
    recommended_projects: List[Dict[str, str]]
    recommended_certifications: List[str]
    suggested_technologies: List[str]
    improvement_priorities: List[Dict[str, str]]

@dataclass
class ImprovedBullet:
    original: str
    improved: str
    improvement_type: str
    explanation: str

# ============== MAIN ANALYZER ==============

class AdvancedResumeAnalyzer:
    def __init__(self, resume_text: str, job_description: Optional[str] = None):
        self.resume_text = resume_text
        self.job_description = job_description or ""
        self.word_count = len(resume_text.split())
        self.lines = resume_text.split('\n')
        
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis and return comprehensive results"""
        
        # Run all analysis modules
        seniority = self.classify_seniority()
        scores = self.calculate_detailed_scores()
        keywords = self.analyze_keywords()
        structure = self.analyze_structure()
        experience = self.analyze_experience_quality()
        technical = self.analyze_technical_stack()
        writing = self.analyze_writing_quality()
        
        # Job description analysis if provided
        job_analysis = None
        if self.job_description:
            job_analysis = self.analyze_job_description()
        
        recruiter = self.simulate_recruiter_review(structure, experience, technical, writing)
        missing_skills = self.detect_missing_skills(technical, experience)
        career_guidance = self.generate_career_guidance(seniority, technical, experience)
        improvements = self.generate_improvements()
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(scores)
        
        return {
            "overall_score": overall_score,
            "seniority_classification": asdict(seniority),
            "score_categories": {s.name: asdict(s) for s in scores},
            "keyword_analysis": asdict(keywords),
            "resume_structure": asdict(structure),
            "experience_quality": asdict(experience),
            "technical_analysis": asdict(technical),
            "writing_quality": asdict(writing),
            "job_analysis": asdict(job_analysis) if job_analysis else None,
            "recruiter_simulation": asdict(recruiter),
            "missing_skills": asdict(missing_skills),
            "career_guidance": asdict(career_guidance),
            "improved_bullets": [asdict(b) for b in improvements],
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def classify_seniority(self) -> SeniorityClassification:
        """Classify candidate into seniority level based on multiple factors"""
        
        score = 0
        max_score = 100
        
        # Factor 1: Word count and depth (15 points)
        if self.word_count > 1500:
            score += 15
        elif self.word_count > 1000:
            score += 10
        elif self.word_count > 500:
            score += 5
        
        # Factor 2: Technical skills depth (20 points)
        tech_count = sum([
            len(re.findall(r'\b' + lang + r'\b', self.resume_text.lower()))
            for lang in TECH_CATEGORIES["programming_languages"]
        ])
        score += min(20, tech_count * 2)
        
        # Factor 3: Leadership indicators (15 points)
        leadership_verbs = [v for v in ACTION_VERBS["leadership"] 
                           if v in self.resume_text.lower()]
        score += min(15, len(leadership_verbs) * 3)
        
        # Factor 4: Achievement metrics (15 points)
        metrics = re.findall(r'\d+%|\$\d+|\d+x|\d+\s*(year|month|day)', self.resume_text.lower())
        score += min(15, len(metrics) * 3)
        
        # Factor 5: Project complexity (15 points)
        complex_terms = ["architecture", "design", "implementation", "deployment", "production"]
        complex_count = sum(1 for t in complex_terms if t in self.resume_text.lower())
        score += min(15, complex_count * 3)
        
        # Factor 6: Experience indicators (10 points)
        exp_indicators = re.findall(r'(\d+)\+?\s*(year|years|yr|yrs)\s*(?:of)?\s*(?:experience|exp)', 
                                   self.resume_text.lower())
        if exp_indicators:
            years = max([int(e[0]) for e in exp_indicators])
            if years >= 7:
                score += 10
            elif years >= 5:
                score += 8
            elif years >= 3:
                score += 5
            elif years >= 1:
                score += 3
        
        # Factor 7: Education and certifications (10 points)
        edu_terms = ["phd", "master", "bachelor", "certification", "certified"]
        if any(t in self.resume_text.lower() for t in edu_terms):
            score += 10
        
        # Determine level
        level_index = min(7, max(0, int(score / 12)))
        level = SENIORITY_LEVELS[level_index]
        confidence = min(95, max(30, score))
        
        # Generate explanation
        explanation = self._generate_level_explanation(level, score)
        
        # Strengths and weaknesses
        strengths = []
        if tech_count >= 5:
            strengths.append("Strong technical skill set")
        if len(metrics) >= 3:
            strengths.append("Quantifiable achievements")
        if len(leadership_verbs) >= 2:
            strengths.append("Leadership experience")
        if complex_count >= 3:
            strengths.append("Complex project involvement")
            
        weaknesses = []
        if self.word_count < 500:
            weaknesses.append("Limited content depth")
        if tech_count < 3:
            weaknesses.append("Narrow technical breadth")
        if len(metrics) < 2:
            weaknesses.append("Few measurable achievements")
        if len(leadership_verbs) < 1:
            weaknesses.append("No clear leadership examples")
        
        # Next level requirements
        next_reqs = self._get_next_level_requirements(level)
        
        return SeniorityClassification(
            level=level,
            confidence_score=confidence,
            explanation=explanation,
            strengths=strengths,
            weaknesses=weaknesses,
            next_level_requirements=next_reqs
        )
    
    def _generate_level_explanation(self, level: str, score: int) -> str:
        """Generate detailed explanation for the classified level"""

        measurable_achievements_count = len(
            re.findall(r"\d+%|\$\d+", self.resume_text)
        )

        explanations = {
            "Rookie": (
                f"Based on the resume content, this candidate appears to be at an "
                f"entry-level stage with limited professional experience. "
                f"The content score of {score}/100 suggests foundational skills "
                f"are being developed. Focus on building strong fundamentals "
                f"and gaining practical experience."
            ),

            "Beginner": (
                f"This candidate shows developing skills with some relevant knowledge. "
                f"A score of {score}/100 indicates they're moving beyond basics "
                f"but still building expertise. Consider junior-level positions "
                f"that offer learning opportunities."
            ),

            "Fresher": (
                f"The resume suggests a recent graduate or early career professional. "
                f"With {self.word_count} words of content, there's evidence of "
                f"academic preparation. Target entry-level roles that provide "
                f"growth potential."
            ),

            "Junior": (
                f"This candidate has some professional experience and foundational skills. "
                f"The score of {score}/100 shows capability for junior responsibilities. "
                f"Look for roles that can leverage existing knowledge while developing further."
            ),

            "Intermediate": (
                f"A solid skill foundation with {self.word_count} words of demonstrated experience. "
                f"This candidate can handle moderate complexity work independently. "
                f"Suitable for mid-level positions with appropriate guidance."
            ),

            "Professional": (
                f"This resume demonstrates proven capabilities with "
                f"{measurable_achievements_count} measurable achievements. "
                f"The candidate can contribute immediately in suitable roles. "
                f"Consider positions requiring independent execution."
            ),

            "Senior": (
                f"Strong technical depth and leadership indicators suggest "
                f"senior-level capability. The comprehensive content demonstrates "
                f"ability to handle complex challenges. Ready for leadership roles "
                f"with minimal supervision."
            ),

            "Expert": (
                f"Exceptional profile with extensive technical expertise and proven impact. "
                f"This candidate can drive technical strategy and lead teams effectively. "
                f"Suitable for principal or leadership positions."
            )
        }

        return explanations.get(level, explanations["Intermediate"])
    
    def _get_next_level_requirements(self, current_level: str) -> List[str]:
        """Get requirements to reach the next seniority level"""
        requirements = {
            "Rookie": [
                "Complete at least 1-2 relevant projects",
                "Gain basic industry tool proficiency",
                "Build foundational understanding of domain"
            ],
            "Beginner": [
                "Accumulate 6-12 months of professional experience",
                "Develop proficiency in 2-3 core technologies",
                "Complete a portfolio of personal projects"
            ],
            "Fresher": [
                "Gain 1-2 years of industry experience",
                "Add 2-3 certifications to credentials",
                "Develop measurable achievements in role"
            ],
            "Junior": [
                "Build 2-3 years of professional experience",
                "Expand technical stack to 5+ technologies",
                "Take on project leadership responsibilities"
            ],
            "Intermediate": [
                "Achieve 3-5 years of relevant experience",
                "Develop expertise in domain-specific technologies",
                "Lead at least one significant project"
            ],
            "Professional": [
                "Accumulate 5-7 years of proven experience",
                "Obtain senior-level certifications",
                "Demonstrate team leadership and mentoring"
            ],
            "Senior": [
                "Build 7-10 years of deep expertise",
                "Contribute to open source or technical publications",
                "Take on architectural or team lead roles"
            ],
            "Expert": [
                "Maintain thought leadership in domain",
                "Drive technical strategy at organization level",
                "Mentor senior engineers and influence hiring"
            ]
        }
        return requirements.get(current_level, requirements["Professional"])
    
    def calculate_detailed_scores(self) -> List[ScoreCategory]:
        """Calculate detailed scores across multiple categories"""
        
        scores = []
        
        # ATS Compatibility Score
        ats_score = self._calculate_ats_score()
        scores.append(ScoreCategory(
            name="ATS Compatibility",
            score=ats_score["score"],
            max_score=100,
            details=ats_score["details"],
            recommendations=ats_score["recommendations"]
        ))
        
        # Technical Skills Score
        tech_score = self._calculate_tech_score()
        scores.append(ScoreCategory(
            name="Technical Skills",
            score=tech_score["score"],
            max_score=100,
            details=tech_score["details"],
            recommendations=tech_score["recommendations"]
        ))
        
        # Project Quality Score
        project_score = self._calculate_project_score()
        scores.append(ScoreCategory(
            name="Project Quality",
            score=project_score["score"],
            max_score=100,
            details=project_score["details"],
            recommendations=project_score["recommendations"]
        ))
        
        # Experience Score
        exp_score = self._calculate_experience_score()
        scores.append(ScoreCategory(
            name="Experience",
            score=exp_score["score"],
            max_score=100,
            details=exp_score["details"],
            recommendations=exp_score["recommendations"]
        ))
        
        # Resume Writing Score
        writing_score = self._calculate_writing_score()
        scores.append(ScoreCategory(
            name="Resume Writing",
            score=writing_score["score"],
            max_score=100,
            details=writing_score["details"],
            recommendations=writing_score["recommendations"]
        ))
        
        # Job Match Score (if job description provided)
        if self.job_description:
            job_score = self._calculate_job_match_score()
            scores.append(ScoreCategory(
                name="Job Match",
                score=job_score["score"],
                max_score=100,
                details=job_score["details"],
                recommendations=job_score["recommendations"]
            ))
        
        # Recruiter Appeal Score
        recruiter_score = self._calculate_recruiter_appeal()
        scores.append(ScoreCategory(
            name="Recruiter Appeal",
            score=recruiter_score["score"],
            max_score=100,
            details=recruiter_score["details"],
            recommendations=recruiter_score["recommendations"]
        ))
        
        return scores
    
    def _calculate_ats_score(self) -> Dict[str, Any]:
        score = 50
        details = []
        recommendations = []
        
        # Check for contact info
        if re.search(r'\S+@\S+\.\S+', self.resume_text):
            score += 10
            details.append("Email detected")
        else:
            recommendations.append("Add a professional email address")
            
        if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', self.resume_text):
            score += 5
            details.append("Phone number detected")
        
        # Check section structure
        sections = self._detect_sections()
        score += min(20, len(sections) * 4)
        details.append(f"{len(sections)} sections detected: {', '.join(sections)}")
        
        if len(sections) < 4:
            recommendations.append("Add standard sections: Summary, Experience, Education, Skills")
        
        # Check for ATS-friendly formatting
        if len(re.findall(r'[#*_~`]|\\section|\\begin', self.resume_text)) > 5:
            score -= 10
            details.append("Potential ATS-unfriendly formatting detected")
            recommendations.append("Avoid special characters and complex formatting")
        
        # Check for reasonable length
        if 400 < self.word_count < 1500:
            score += 10
            details.append("Optimal resume length")
        elif self.word_count < 400:
            score -= 10
            recommendations.append("Resume is too short - add more detail")
        elif self.word_count > 2000:
            score -= 5
            recommendations.append("Consider trimming to most relevant information")
        
        return {"score": max(0, min(100, score)), "details": details, "recommendations": recommendations}
    
    def _calculate_tech_score(self) -> Dict[str, Any]:
        score = 20
        details = []
        recommendations = []
        
        text_lower = self.resume_text.lower()
        
        # Count technologies in each category
        for category, technologies in TECH_CATEGORIES.items():
            found = [t for t in technologies if t in text_lower]
            if found:
                score += len(found) * 2
                details.append(f"{category.replace('_', ' ').title()}: {', '.join(found[:5])}")
        
        # Check for modern technologies
        modern = ["react", "typescript", "aws", "docker", "kubernetes", "python", "machine learning"]
        modern_count = sum(1 for t in modern if t in text_lower)
        score += modern_count * 2
        
        if modern_count < 3:
            recommendations.append("Add more modern, in-demand technologies")
        
        return {"score": min(100, score), "details": details, "recommendations": recommendations}
    
    def _calculate_project_score(self) -> Dict[str, Any]:
        score = 30
        details = []
        recommendations = []
        
        # Check for project descriptions
        project_patterns = [r'project\s+[:\-]?\s*(\w+)', r'built\s+(\w+)', r'developed\s+(\w+)']
        projects = []
        for pattern in project_patterns:
            projects.extend(re.findall(pattern, self.resume_text.lower()))
        
        if projects:
            score += min(20, len(projects) * 5)
            details.append(f"{len(projects)} projects described")
        
        # Check for technical complexity indicators
        complexity_words = ["architecture", "design pattern", "api", "database", "frontend", "backend", "deployment"]
        complexity_count = sum(1 for w in complexity_words if w in self.resume_text.lower())
        score += min(25, complexity_count * 5)
        
        if complexity_count < 3:
            recommendations.append("Add more technical details about project architecture and challenges")
        
        # Check for metrics in projects
        project_sections = re.findall(r'project[s]?[:\s]([^.]+)', self.resume_text, re.IGNORECASE)
        metrics_in_projects = sum(1 for ps in project_sections if re.search(r'\d+%|\$\d+|\d+x', ps))
        if metrics_in_projects:
            score += 15
            details.append(f"{metrics_in_projects} projects have quantifiable metrics")
        
        return {"score": min(100, score), "details": details, "recommendations": recommendations}
    
    def _calculate_experience_score(self) -> Dict[str, Any]:
        score = 30
        details = []
        recommendations = []
        
        # Check for job history length
        job_titles = re.findall(r'(?:software|engineer|developer|analyst|manager|lead|architect)\s+\w+', 
                               self.resume_text.lower())
        if job_titles:
            score += min(20, len(job_titles) * 5)
            details.append(f"{len(job_titles)} position titles detected")
        
        # Check for quantifiable achievements
        achievements = re.findall(r'\d+%|\$\d+|\d+x|\d+\s*(?:users|clients|employees|sales)', self.resume_text)
        score += min(25, len(achievements) * 5)
        
        if achievements:
            details.append(f"{len(achievements)} quantifiable achievements found")
        
        if len(achievements) < 3:
            recommendations.append("Add more quantifiable results (percentages, dollar amounts, scale)")
        
        # Check for leadership indicators
        leadership = [v for v in ACTION_VERBS["leadership"] if v in self.resume_text.lower()]
        score += min(15, len(leadership) * 5)
        
        if leadership:
            details.append(f"Leadership verbs found: {', '.join(leadership)}")
        
        return {"score": min(100, score), "details": details, "recommendations": recommendations}
    
    def _calculate_writing_score(self) -> Dict[str, Any]:
        score = 70
        details = []
        recommendations = []
        
        text_lower = self.resume_text.lower()
        
        # Check for weak phrases
        weak_count = sum(1 for wp in WEAK_PHRASES if wp in text_lower)
        score -= weak_count * 3
        
        if weak_count > 0:
            details.append(f"{weak_count} weak phrases detected")
            recommendations.append("Replace weak phrases with stronger action verbs")
        
        # Check for passive voice
        passive_count = sum(1 for pp in PASSIVE_PHRASES if pp in text_lower)
        score -= passive_count * 5
        
        if passive_count > 0:
            details.append(f"{passive_count} passive voice instances")
            recommendations.append("Use active voice instead of passive constructions")
        
        # Check for action verbs
        action_verbs_found = []
        for category, verbs in ACTION_VERBS.items():
            for verb in verbs:
                if verb in text_lower:
                    action_verbs_found.append(verb)
        
        score += min(15, len(action_verbs_found) * 2)
        
        if action_verbs_found:
            details.append(f"{len(action_verbs_found)} action verbs used")
        
        if len(action_verbs_found) < 5:
            recommendations.append("Use more strong action verbs to describe accomplishments")
        
        # Check for bullet points
        bullet_points = re.findall(r'[•\-\*]\s+\w+', self.resume_text)
        if len(bullet_points) > 5:
            score += 10
            details.append(f"{len(bullet_points)} bullet points found")
        
        return {"score": max(0, min(100, score)), "details": details, "recommendations": recommendations}
    
    def _calculate_job_match_score(self) -> Dict[str, Any]:
        score = 50
        details = []
        recommendations = []
        
        job_text_lower = self.job_description.lower()
        resume_text_lower = self.resume_text.lower()
        
        # Extract job keywords
        job_keywords = set(re.findall(r'\b[a-z]{3,}\b', job_text_lower))
        resume_keywords = set(re.findall(r'\b[a-z]{3,}\b', resume_text_lower))
        
        # Common technical terms to focus on
        tech_terms = []
        for category in TECH_CATEGORIES.values():
            tech_terms.extend(category)
        
        job_tech = set([t for t in tech_terms if t in job_text_lower])
        resume_tech = set([t for t in tech_terms if t in resume_text_lower])
        
        if job_tech:
            match_ratio = len(resume_tech & job_tech) / len(job_tech)
            score = int(match_ratio * 80) + 20
            details.append(f"Technical skill match: {int(match_ratio * 100)}%")
            
            missing = list(job_tech - resume_tech)
            if missing:
                recommendations.append(f"Add these missing skills: {', '.join(missing[:5])}")
        
        return {"score": max(0, min(100, score)), "details": details, "recommendations": recommendations}
    
    def _calculate_recruiter_appeal(self) -> Dict[str, Any]:
        score = 60
        details = []
        recommendations = []
        
        text_lower = self.resume_text.lower()
        
        # Check for summary/objective
        if re.search(r'summary|objective|profile', text_lower):
            score += 10
            details.append("Has professional summary")
        else:
            recommendations.append("Add a strong professional summary at the top")
        
        # Check for quantifiable impact
        if re.search(r'\d+%|\$[\d,]+|\d+x', self.resume_text):
            score += 10
            details.append("Shows measurable impact")
        
        # Check for varied language
        unique_words = len(set(text_lower.split()))
        if unique_words > 100:
            score += 5
            details.append("Good vocabulary variety")
        
        # Check formatting (line breaks, bullets)
        if re.search(r'[\n\-•\*]', self.resume_text):
            score += 10
            details.append("Good use of formatting")
        
        return {"score": min(100, score), "details": details, "recommendations": recommendations}
    
    def analyze_keywords(self) -> KeywordAnalysis:
        """Analyze keywords in detail"""
        text_lower = self.resume_text.lower()
        job_lower = self.job_description.lower() if self.job_description else ""
        
        # Exact matches from job description
        exact_matches = []
        if job_lower:
            job_words = re.findall(r'\b[a-z]{3,}\b', job_lower)
            for word in job_words:
                if word in text_lower and word not in exact_matches:
                    exact_matches.append(word)
        
        # Semantic matches (related terms)
        semantic_map = {
            "python": ["django", "flask", "pandas", "numpy", "jupyter"],
            "javascript": ["node", "react", "vue", "typescript", "jquery"],
            "java": ["spring", "maven", "hibernate", "junit"],
            "aws": ["ec2", "s3", "lambda", "dynamodb", "cloudformation"],
            "machine learning": ["deep learning", "tensorflow", "pytorch", "neural"]
        }
        
        semantic_matches = []
        for main, related in semantic_map.items():
            if main in text_lower:
                for r in related:
                    if r in text_lower and r not in semantic_matches:
                        semantic_matches.append(r)
        
        # Missing critical keywords
        missing_critical = []
        if job_lower:
            critical_terms = ["experience", "skills", "knowledge", "work", "developed"]
            for term in critical_terms:
                if term in job_lower and term not in text_lower:
                    missing_critical.append(term)
        
        # Calculate match percentage
        if job_lower:
            job_tokens = set(re.findall(r'\b[a-z]{4,}\b', job_lower))
            resume_tokens = set(re.findall(r'\b[a-z]{4,}\b', text_lower))
            match_pct = len(job_tokens & resume_tokens) / len(job_tokens) * 100 if job_tokens else 0
        else:
            match_pct = 75  # Default when no job description
        
        return KeywordAnalysis(
            exact_matches=exact_matches[:20],
            semantic_matches=semantic_matches[:10],
            missing_critical=missing_critical[:10],
            match_percentage=round(match_pct, 1)
        )
    
    def analyze_structure(self) -> ResumeStructure:
        """Analyze resume structure and formatting"""
        text_lower = self.resume_text.lower()
        
        # Detect sections
        section_keywords = {
            "summary": ["summary", "objective", "profile", "about"],
            "experience": ["experience", "employment", "work history", "professional experience"],
            "education": ["education", "academic", "degree", "university", "college"],
            "skills": ["skills", "technical skills", "technologies", "competencies"],
            "projects": ["projects", "portfolio", "personal projects"]
        }
        
        found_sections = {}
        for section, keywords in section_keywords.items():
            found_sections[section] = any(k in text_lower for k in keywords)
        
        structure = ResumeStructure(
            has_contact_info=bool(re.search(r'\S+@\S+\.\S+', self.resume_text)),
            has_summary=found_sections["summary"],
            has_experience=found_sections["experience"],
            has_education=found_sections["education"],
            has_skills=found_sections["skills"],
            has_projects=found_sections["projects"],
            section_count=sum(found_sections.values()),
            readability_score=self._calculate_readability(),
            formatting_issues=self._detect_formatting_issues()
        )
        
        return structure
    
    def _calculate_readability(self) -> int:
        """Calculate readability score"""
        lines = [l for l in self.lines if l.strip()]
        if not lines:
            return 0
        
        avg_line_length = sum(len(l) for l in lines) / len(lines)
        
        # Score based on line length (shorter lines = more readable)
        if 40 < avg_line_length < 80:
            return 85
        elif 30 < avg_line_length < 100:
            return 70
        else:
            return 50
    
    def _detect_formatting_issues(self) -> List[str]:
        """Detect formatting issues that hurt ATS"""
        issues = []
        
        # Check for tables (ATS can't read)
        if "|" in self.resume_text or re.search(r'\|.*\|', self.resume_text):
            issues.append("Tables may not be parsed correctly by ATS")
        
        # Check for headers in wrong format
        if re.search(r'^[A-Z][A-Z\s]{10,}$', self.resume_text, re.MULTILINE):
            issues.append("Text-only headers may not be detected")
        
        # Check for special characters
        special_chars = len(re.findall(r'[®©™§¶]', self.resume_text))
        if special_chars > 3:
            issues.append("Too many special characters may confuse ATS")
        
        return issues
    
    def _detect_sections(self) -> List[str]:
        """Detect which sections exist in the resume"""
        text_lower = self.resume_text.lower()
        sections = []
        
        section_markers = {
            "Summary": ["summary", "objective", "profile"],
            "Experience": ["experience", "employment", "work history"],
            "Education": ["education", "academic"],
            "Skills": ["skills", "technical", "technologies"],
            "Projects": ["projects", "portfolio"]
        }
        
        for section, markers in section_markers.items():
            if any(m in text_lower for m in markers):
                sections.append(section)
        
        return sections
    
    def analyze_experience_quality(self) -> ExperienceQuality:
        """Analyze the quality of experience descriptions"""
        text_lower = self.resume_text.lower()
        
        # Find measurable achievements
        achievements = re.findall(
            r'(\d+%|\$\d+[\d,]*|\d+x|\d+\s*(?:users|clients|employees|sales|performance|speed|accuracy|growth|improvement))',
            self.resume_text,
            re.IGNORECASE
        )
        
        # Find leadership indicators
        leadership = []
        for verb in ACTION_VERBS["leadership"]:
            if re.search(rf'\b{verb}\b', text_lower):
                leadership.append(verb)
        
        # Find project complexity indicators
        complexity = []
        complex_terms = {
            "Architecture": ["architecture", "design pattern", "system design"],
            "Scale": ["scalable", "high traffic", "million", "billion"],
            "API": ["rest api", "graphql", "microservice"],
            "Database": ["database", "schema", "optimization"],
            "Cloud": ["cloud", "aws", "azure", "gcp", "deployment"]
        }
        
        for term_type, terms in complex_terms.items():
            for term in terms:
                if term in text_lower:
                    complexity.append(term_type)
                    break
        
        # Find impact statements
        impact_keywords = ["increased", "decreased", "improved", "reduced", "saved", "generated", "delivered"]
        impact_statements = [k for k in impact_keywords if k in text_lower]
        
        # Calculate quality score
        quality_score = min(100, 
            len(achievements) * 8 + 
            len(leadership) * 10 + 
            len(complexity) * 7 +
            len(impact_statements) * 5
        )
        
        return ExperienceQuality(
            measurable_achievements=achievements[:10],
            leadership_indicators=leadership[:5],
            project_complexity=list(set(complexity))[:5],
            impact_statements=impact_statements[:5],
            quality_score=quality_score
        )
    
    def analyze_technical_stack(self) -> TechnicalAnalysis:
        """Analyze the technical stack"""
        text_lower = self.resume_text.lower()
        
        found_tech = {category: [] for category in TECH_CATEGORIES}
        
        for category, technologies in TECH_CATEGORIES.items():
            for tech in technologies:
                if re.search(rf'\b{re.escape(tech)}\b', text_lower):
                    found_tech[category].append(tech)
        
        # Determine maturity level
        total_tech = sum(len(v) for v in found_tech.values())
        if total_tech >= 15:
            maturity = "Expert"
        elif total_tech >= 10:
            maturity = "Advanced"
        elif total_tech >= 5:
            maturity = "Intermediate"
        else:
            maturity = "Beginner"
        
        return TechnicalAnalysis(
            programming_languages=found_tech["programming_languages"],
            frameworks=found_tech["frameworks"],
            databases=found_tech["databases"],
            cloud_devops=found_tech["cloud_devops"],
            ai_ml_tools=found_tech["ai_ml"],
            other_technologies=found_tech["other_tech"],
            maturity_level=maturity
        )
    
    def analyze_writing_quality(self) -> WritingQuality:
        """Analyze writing quality"""
        text_lower = self.resume_text.lower()
        
        # Find weak phrases
        weak_found = [wp for wp in WEAK_PHRASES if wp in text_lower]
        
        # Find passive voice
        passive_found = [pp for pp in PASSIVE_PHRASES if pp in text_lower]
        
        # Find vague descriptions
        vague_terms = ["good", "great", "excellent", "some", "various", "many"]
        vague_found = [v for v in vague_terms if re.search(rf'\b{v}\b', text_lower)]
        
        # Calculate score
        score = 100 - len(weak_found) * 5 - len(passive_found) * 5 - len(vague_found) * 2
        
        return WritingQuality(
            grammar_issues=[],  # Would need NLP for proper grammar check
            weak_phrases=list(set(weak_found))[:5],
            passive_voice_count=len(passive_found),
            repetitive_language=[],  # Would need more complex analysis
            vague_descriptions=list(set(vague_found))[:5],
            overall_score=max(0, min(100, score))
        )
    
    def analyze_job_description(self) -> JobAnalysis:
        """Analyze job description and compare with resume"""
        job_lower = self.job_description.lower()
        resume_lower = self.resume_text.lower()
        
        # Extract skills from job description
        extracted_skills = []
        for category, technologies in TECH_CATEGORIES.items():
            for tech in technologies:
                if tech in job_lower:
                    extracted_skills.append(tech)
        
        # Detect seniority requirement
        seniority_keywords = {
            "Entry": ["entry", "junior", "fresher", "graduate", "intern"],
            "Mid": ["intermediate", "mid-level", "3-5 years"],
            "Senior": ["senior", "5+ years", "7+ years", "experienced"],
            "Lead": ["lead", "principal", "staff", "architect", "10+ years"]
        }
        
        seniority_requirement = "Mid-Level"
        for level, keywords in seniority_keywords.items():
            if any(k in job_lower for k in keywords):
                seniority_requirement = level
                break
        
        # Hidden expectations
        hidden = []
        if "fast-paced" in job_lower:
            hidden.append("Ability to handle multiple priorities")
        if "startup" in job_lower or "growth" in job_lower:
            hidden.append("Comfortable with ambiguity and change")
        if "cross-functional" in job_lower:
            hidden.append("Strong communication skills needed")
        
        # Match percentage
        matched_skills = [s for s in extracted_skills if s in resume_lower]
        match_pct = len(matched_skills) / len(extracted_skills) * 100 if extracted_skills else 75
        
        # Missing skills
        missing_skills = list(set(extracted_skills) - set(matched_skills))
        
        # Candidate fit
        if match_pct >= 70:
            fit = "Strong match - proceed with strong consideration"
        elif match_pct >= 50:
            fit = "Moderate match - worth interviewing for related role"
        else:
            fit = "Weak match - consider for similar but different role"
        
        return JobAnalysis(
            extracted_skills=extracted_skills[:15],
            seniority_requirement=seniority_requirement,
            hidden_expectations=hidden[:5],
            match_percentage=round(match_pct, 1),
            candidate_fit=fit,
            missing_skills=missing_skills[:10]
        )
    
    def simulate_recruiter_review(self, structure: ResumeStructure, 
                                   experience: ExperienceQuality,
                                   technical: TechnicalAnalysis,
                                   writing: WritingQuality) -> RecruiterSimulation:
        """Simulate what a recruiter would think"""
        
        text_lower = self.resume_text.lower()
        
        # First impression
        first_impression = "Professional resume with clear structure"
        if structure.section_count >= 4:
            first_impression += ". Well-organized sections make it easy to scan."
        if experience.quality_score >= 70:
            first_impression += " Shows clear achievements and impact."
        
        # Strengths
        strengths = []
        if technical.programming_languages:
            strengths.append(f"Solid technical foundation with {len(technical.programming_languages)} technologies")
        if experience.measurable_achievements:
            strengths.append("Includes quantifiable achievements")
        if experience.leadership_indicators:
            strengths.append("Shows leadership potential")
        if structure.has_summary:
            strengths.append("Professional summary provides quick context")
        
        # Red flags
        red_flags = []
        if self.word_count < 300:
            red_flags.append("Too little content - may lack experience")
        if self.word_count > 2000:
            red_flags.append("Too much content - may need trimming")
        if writing.weak_phrases:
            red_flags.append(f"Weak language: {', '.join(writing.weak_phrases[:2])}")
        if len(technical.programming_languages) < 2:
            red_flags.append("Limited technical skills demonstrated")
        
        # Missing information
        missing = []
        if not structure.has_summary:
            missing.append("Professional summary")
        if not structure.has_skills:
            missing.append("Technical skills section")
        if not experience.measurable_achievements:
            missing.append("Quantifiable achievements")
        
        # Hiring likelihood
        if len(red_flags) <= 1 and experience.quality_score >= 60:
            hiring_likelihood = "High - Strong candidate"
        elif len(red_flags) <= 2:
            hiring_likelihood = "Medium - Some concerns to address"
        else:
            hiring_likelihood = "Low - Significant improvements needed"
        
        # Interview probability
        interview_prob = "85%" if structure.section_count >= 4 and experience.quality_score >= 60 else "60%"
        
        # Quick notes
        notes = f"Overall: {experience.quality_score}/100 quality score. "
        notes += f"Technical maturity: {technical.maturity_level}. "
        notes += f"Writing clarity: {writing.overall_score}/100."
        
        return RecruiterSimulation(
            first_impression=first_impression,
            strengths=strengths[:5],
            red_flags=red_flags[:5],
            missing_information=missing[:5],
            hiring_likelihood=hiring_likelihood,
            interview_probability=interview_prob,
            quick_notes=notes
        )
    
    def detect_missing_skills(self, technical: TechnicalAnalysis,
                              experience: ExperienceQuality) -> MissingSkills:
        """Detect skills and experiences that are missing"""
        
        # Missing technologies
        missing_tech = []
        essential_tech = ["python", "javascript", "sql", "git", "docker"]
        for tech in essential_tech:
            if not any(tech in getattr(technical, cat) for cat in ["programming_languages", "frameworks", "cloud_devops"]):
                missing_tech.append(tech)
        
        # Missing certifications
        cert_keywords = ["certified", "certification", "aws certified", "google certified", "microsoft certified"]
        has_cert = any(c in self.resume_text.lower() for c in cert_keywords)
        missing_certs = [] if has_cert else ["Industry certifications recommended"]
        
        # Leadership gaps
        leadership_gaps = []
        if not experience.leadership_indicators:
            leadership_gaps.append("No clear leadership responsibilities demonstrated")
        if len(experience.leadership_indicators) < 2:
            leadership_gaps.append("Limited leadership examples")
        
        # Experience gaps
        exp_gaps = []
        if not experience.measurable_achievements:
            exp_gaps.append("No quantifiable achievements")
        if len(experience.measurable_achievements) < 3:
            exp_gaps.append("Need more results-driven accomplishments")
        
        # Metrics gaps
        metrics_gaps = []
        if not experience.impact_statements:
            metrics_gaps.append("No impact statements found")
        
        return MissingSkills(
            technologies=missing_tech[:10],
            certifications=missing_certs[:5],
            leadership_gaps=leadership_gaps[:5],
            experience_gaps=exp_gaps[:5],
            metrics_gaps=metrics_gaps[:5]
        )
    
    def generate_career_guidance(self, seniority: SeniorityClassification,
                                  technical: TechnicalAnalysis,
                                  experience: ExperienceQuality) -> CareerGuidance:
        """Generate career guidance and roadmap"""
        
        current_level = seniority.level
        next_level_index = SENIORITY_LEVELS.index(current_level) + 1
        next_level = SENIORITY_LEVELS[min(next_level_index, 7)]
        
        # Roadmap
        roadmap = [
            {"phase": "1-3 months", "action": f"Address key weaknesses identified in analysis"},
            {"phase": "3-6 months", "action": f"Build skills for {next_level} role"},
            {"phase": "6-12 months", "action": "Apply to positions at next level"},
            {"phase": "1-2 years", "action": f"Transition to {next_level} position"}
        ]
        
        # Recommended projects
        projects = []
        if "python" in technical.programming_languages or "javascript" in technical.programming_languages:
            projects.append({
                "title": "Full-stack Application",
                "description": "Build a complete web application with database, API, and frontend"
            })
        if "aws" in technical.cloud_devops or "azure" in technical.cloud_devops:
            projects.append({
                "title": "Cloud Infrastructure Project",
                "description": "Design and deploy scalable cloud infrastructure"
            })
        projects.append({
            "title": "Open Source Contribution",
            "description": "Contribute to open source projects in your domain"
        })
        
        # Recommended certifications
        certs = []
        if any(t in technical.ai_ml_tools for t in ["machine learning", "deep learning"]):
            certs.append("AWS Machine Learning Specialty")
        if "aws" in technical.cloud_devops:
            certs.append("AWS Solutions Architect")
        certs.extend(["Professional Scrum Master", "System Design Certification"])
        
        # Suggested technologies
        suggestions = []
        if "python" not in technical.programming_languages:
            suggestions.append("Python")
        if "react" not in technical.frameworks:
            suggestions.append("React")
        if "aws" not in technical.cloud_devops:
            suggestions.append("AWS/Cloud")
        if "docker" not in technical.cloud_devops:
            suggestions.append("Docker")
        suggestions.extend(["System Design", "CI/CD", "Testing"])
        
        # Improvement priorities
        priorities = []
        if seniority.weaknesses:
            priorities.append({"priority": "High", "area": f"Fix: {seniority.weaknesses[0]}"})
        if experience.measurable_achievements:
            priorities.append({"priority": "Medium", "area": "Add more quantifiable achievements"})
        if technical.maturity_level in ["Beginner", "Intermediate"]:
            priorities.append({"priority": "Medium", "area": "Deepen technical expertise"})
        priorities.append({"priority": "Low", "area": "Continue building portfolio"})
        
        return CareerGuidance(
            roadmap_to_next_level=roadmap,
            recommended_projects=projects[:5],
            recommended_certifications=certs[:5],
            suggested_technologies=suggestions[:10],
            improvement_priorities=priorities[:5]
        )
    
    def generate_improvements(self) -> List[ImprovedBullet]:
        """Generate improved resume bullets"""
        
        # Find potential bullets to improve
        bullet_candidates = re.findall(r'[-•*]\s+([^.\n]+)', self.resume_text)
        
        improvements = []
        
        if not bullet_candidates:
            # Try to find experience descriptions
            bullet_candidates = re.findall(
                r'(?:worked|responsible|managed|led|developed|created)[^.]+',
                self.resume_text.lower()
            )[:5]
        
        for original in bullet_candidates[:5]:
            # Analyze the original
            original_clean = original.strip()
            
            # Determine improvement type
            improvement_type = "general"
            if any(wp in original_clean for wp in WEAK_PHRASES):
                improvement_type = "strengthen_action"
            elif not re.search(r'\d+', original_clean):
                improvement_type = "add_metrics"
            elif "and" in original_clean and len(original_clean.split()) > 15:
                improvement_type = "concise"
            
            # Generate improved version
            improved = self._improve_bullet(original_clean, improvement_type)
            
            improvements.append(ImprovedBullet(
                original=original_clean[:100],
                improved=improved,
                improvement_type=improvement_type,
                explanation=self._get_improvement_explanation(improvement_type)
            ))
        
        return improvements[:5]
    
    def _improve_bullet(self, original: str, improvement_type: str) -> str:
        """Generate an improved version of a bullet point"""
        
        if improvement_type == "add_metrics":
            # Add metrics to vague descriptions
            if "improved" in original:
                return original + " resulting in 25% performance increase"
            elif "managed" in original:
                return original + " serving 50+ team members"
            elif "developed" in original:
                return original + " used by 1000+ users"
        
        elif improvement_type == "strengthen_action":
            # Replace weak verbs with stronger ones
            replacements = {
                "worked on": "Contributed to",
                "responsible for": "Led",
                "helped with": "Supported",
                "assisted in": "Partnered on"
            }
            for weak, strong in replacements.items():
                if weak in original:
                    return original.replace(weak, strong)
        
        # Default: add impact focus
        if not re.search(r'\d+|resulting|achieving', original):
            return original + " with measurable business impact"
        
        return original
    
    def _get_improvement_explanation(self, improvement_type: str) -> str:
        explanations = {
            "add_metrics": "Added quantifiable metrics to demonstrate measurable impact",
            "strengthen_action": "Replaced weak action verbs with stronger, more impactful language",
            "concise": "Streamlined to focus on key accomplishments",
            "general": "Improved clarity and impact of the statement"
        }
        return explanations.get(improvement_type, explanations["general"])
    
    def calculate_overall_score(self, scores: List[ScoreCategory]) -> int:
        """Calculate weighted overall score"""
        
        # Define weights
        weights = {
            "ATS Compatibility": 0.10,
            "Technical Skills": 0.20,
            "Project Quality": 0.15,
            "Experience": 0.20,
            "Resume Writing": 0.15,
            "Job Match": 0.10,
            "Recruiter Appeal": 0.10
        }
        
        total_weight = 0
        weighted_sum = 0
        
        for score in scores:
            weight = weights.get(score.name, 0.10)
            weighted_sum += (score.score / score.max_score) * 100 * weight
            total_weight += weight
        
        # If no job description, redistribute weights
        if total_weight < 0.9:
            weighted_sum = weighted_sum / total_weight * 0.9 if total_weight > 0 else weighted_sum
        
        return int(weighted_sum)


# ============== HELPER FUNCTION ==============

def analyze_resume(resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
    """Main entry point for resume analysis"""
    analyzer = AdvancedResumeAnalyzer(resume_text, job_description)
    return analyzer.analyze()
