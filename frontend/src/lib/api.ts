const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8001/api/v1";

export type Resume = {
  id: string;
  filename: string;
  uploaded_at: string;
  extracted_text?: string | null;
};

export type JobDescription = {
  id: string;
  title: string;
  description_text: string;
  uploaded_at: string;
};

export type SeniorityClassification = {
  level: string;
  confidence_score: number;
  explanation: string;
  strengths: string[];
  weaknesses: string[];
  next_level_requirements: string[];
};

export type ScoreCategory = {
  name: string;
  score: number;
  max_score: number;
  details: string[];
  recommendations: string[];
};

export type KeywordAnalysis = {
  exact_matches: string[];
  semantic_matches: string[];
  missing_critical: string[];
  match_percentage: number;
};

export type ResumeStructure = {
  has_contact_info: boolean;
  has_summary: boolean;
  has_experience: boolean;
  has_education: boolean;
  has_skills: boolean;
  has_projects: boolean;
  section_count: number;
  readability_score: number;
  formatting_issues: string[];
};

export type ExperienceQuality = {
  measurable_achievements: string[];
  leadership_indicators: string[];
  project_complexity: string[];
  impact_statements: string[];
  quality_score: number;
};

export type TechnicalAnalysis = {
  programming_languages: string[];
  frameworks: string[];
  databases: string[];
  cloud_devops: string[];
  ai_ml_tools: string[];
  other_technologies: string[];
  maturity_level: string;
};

export type WritingQuality = {
  grammar_issues: string[];
  weak_phrases: string[];
  passive_voice_count: number;
  repetitive_language: string[];
  vague_descriptions: string[];
  overall_score: number;
};

export type JobAnalysis = {
  extracted_skills: string[];
  seniority_requirement: string;
  hidden_expectations: string[];
  match_percentage: number;
  candidate_fit: string;
  missing_skills: string[];
};

export type RecruiterSimulation = {
  first_impression: string;
  strengths: string[];
  red_flags: string[];
  missing_information: string[];
  hiring_likelihood: string;
  interview_probability: string;
  quick_notes: string;
};

export type MissingSkills = {
  technologies: string[];
  certifications: string[];
  leadership_gaps: string[];
  experience_gaps: string[];
  metrics_gaps: string[];
};

export type CareerGuidance = {
  roadmap_to_next_level: { phase: string; action: string }[];
  recommended_projects: { title: string; description: string }[];
  recommended_certifications: string[];
  suggested_technologies: string[];
  improvement_priorities: { priority: string; area: string }[];
};

export type ImprovedBullet = {
  original: string;
  improved: string;
  improvement_type: string;
  explanation: string;
};

export type Analysis = {
  id: string;
  resume_id: string;
  job_desc_id?: string | null;
  created_at: string;
  
  // Legacy fields
  ats_score?: number | null;
  keyword_matches?: string[] | null;
  missing_keywords?: string[] | null;
  weak_sections?: Record<string, string> | null;
  suggestions?: string[] | null;
  rewritten_bullets?: string[] | null;
  
  // New comprehensive analysis
  overall_score?: number | null;
  seniority_classification?: SeniorityClassification | null;
  score_categories?: ScoreCategory[] | null;
  keyword_analysis?: KeywordAnalysis | null;
  resume_structure?: ResumeStructure | null;
  experience_quality?: ExperienceQuality | null;
  technical_analysis?: TechnicalAnalysis | null;
  writing_quality?: WritingQuality | null;
  job_analysis?: JobAnalysis | null;
  recruiter_simulation?: RecruiterSimulation | null;
  missing_skills?: MissingSkills | null;
  career_guidance?: CareerGuidance | null;
  improved_bullets?: ImprovedBullet[] | null;
  analysis_timestamp?: string | null;
};

async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  const isFormData = options.body instanceof FormData;
  if (!isFormData && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const payload = await response.json();
      message = payload.detail ?? message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(Array.isArray(message) ? "Please check the form fields." : message);
  }

  return response.json() as Promise<T>;
}

export function signup(email: string, password: string) {
  return apiFetch<{ access_token: string; refresh_token: string }>("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function login(email: string, password: string) {
  const body = new URLSearchParams({ username: email, password });
  return apiFetch<{ access_token: string; refresh_token: string }>("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
}

export function logout() {
  return apiFetch<{ detail: string }>("/auth/logout", { method: "POST" });
}

export function getMe() {
  return apiFetch<{ id: string; email: string }>("/auth/me");
}

export function uploadResume(file: File) {
  const body = new FormData();
  body.append("file", file);
  return apiFetch<Resume>("/resumes/", { method: "POST", body });
}

export function listResumes() {
  return apiFetch<{ resumes: Resume[] }>("/resumes/");
}

export function deleteResume(resumeId: string) {
  return apiFetch<{ detail: string }>(`/resumes/${resumeId}`, { method: "DELETE" });
}

export function createJob(title: string, description: string) {
  return apiFetch<JobDescription>("/jobs/", {
    method: "POST",
    body: JSON.stringify({ title, description }),
  });
}

export function listJobs() {
  return apiFetch<{ jobs: JobDescription[] }>("/jobs/");
}

export function createAnalysis(resumeId: string, jobDescId?: string) {
  return apiFetch<Analysis>("/analyses/", {
    method: "POST",
    body: JSON.stringify({ resume_id: resumeId, job_desc_id: jobDescId || null }),
  });
}

export function listAnalyses() {
  return apiFetch<{ analyses: Analysis[] }>("/analyses/");
}

export function getAnalysis(analysisId: string) {
  return apiFetch<Analysis>(`/analyses/${analysisId}`);
}


