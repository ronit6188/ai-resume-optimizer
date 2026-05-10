"""Typed API endpoint functions."""

import { apiClient } from "./client";


// ============================================================================
// Types
// ============================================================================

export interface User {
  id: string;
  email: string;
}

export interface Resume {
  id: string;
  filename: string;
  uploaded_at: string;
  extracted_text?: string | null;
}

export interface ResumeList {
  resumes: Resume[];
}

export interface JobDescription {
  id: string;
  title: string;
  description_text: string;
  uploaded_at: string;
}

export interface JobList {
  jobs: JobDescription[];
}

export interface Analysis {
  id: string;
  resume_id: string;
  job_desc_id: string | null;
  created_at: string;
  ats_score?: number | null;
  keyword_matches?: Record<string, unknown> | null;
  missing_keywords?: string[] | null;
  weak_sections?: Record<string, unknown> | null;
  suggestions?: string[] | null;
  rewritten_bullets?: string[] | null;
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
}

export interface AnalysisList {
  analyses: Analysis[];
}

export interface SeniorityClassification {
  level: string;
  confidence_score: number;
  explanation: string;
  strengths: string[];
  weaknesses: string[];
  next_level_requirements: string[];
}

export interface ScoreCategory {
  name: string;
  score: number;
  max_score: number;
  details: string[];
  recommendations: string[];
}

export interface KeywordAnalysis {
  exact_matches: string[];
  semantic_matches: string[];
  missing_critical: string[];
  match_percentage: number;
}

export interface ResumeStructure {
  has_contact_info: boolean;
  has_summary: boolean;
  has_experience: boolean;
  has_education: boolean;
  has_skills: boolean;
  has_projects: boolean;
  section_count: number;
  readability_score: number;
  formatting_issues: string[];
}

export interface ExperienceQuality {
  measurable_achievements: string[];
  leadership_indicators: string[];
  project_complexity: string[];
  impact_statements: string[];
  quality_score: number;
}

export interface TechnicalAnalysis {
  programming_languages: string[];
  frameworks: string[];
  databases: string[];
  cloud_devops: string[];
  ai_ml_tools: string[];
  other_technologies: string[];
  maturity_level: string;
}

export interface WritingQuality {
  grammar_issues: string[];
  weak_phrases: string[];
  passive_voice_count: number;
  repetitive_language: string[];
  vague_descriptions: string[];
  overall_score: number;
}

export interface JobAnalysis {
  extracted_skills: string[];
  seniority_requirement: string;
  hidden_expectations: string[];
  match_percentage: number;
  candidate_fit: string;
  missing_skills: string[];
}

export interface RecruiterSimulation {
  first_impression: string;
  strengths: string[];
  red_flags: string[];
  missing_information: string[];
  hiring_likelihood: string;
  interview_probability: string;
  quick_notes: string;
}

export interface MissingSkills {
  technologies: string[];
  certifications: string[];
  leadership_gaps: string[];
  experience_gaps: string[];
  metrics_gaps: string[];
}

export interface CareerGuidance {
  roadmap_to_next_level: Record<string, string>[];
  recommended_projects: Record<string, string>[];
  recommended_certifications: string[];
  suggested_technologies: string[];
  improvement_priorities: Record<string, string>[];
}

export interface ImprovedBullet {
  original: string;
  improved: string;
  improvement_type: string;
  explanation: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
}

export interface MatchResult {
  match_percent: number;
  matched_keywords: string[];
}


// ============================================================================
// Auth Endpoints
// ============================================================================

export async function signup(email: string, password: string): Promise<TokenResponse> {
  return apiClient.post<TokenResponse>("/auth/signup", { email, password });
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);
  
  return apiClient.post<TokenResponse>("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
}

export async function logout(): Promise<void> {
  return apiClient.post<void>("/auth/logout");
}

export async function refreshToken(): Promise<TokenResponse> {
  return apiClient.post<TokenResponse>("/auth/refresh");
}

export async function getMe(): Promise<User> {
  return apiClient.get<User>("/auth/me");
}


// ============================================================================
// Resume Endpoints
// ============================================================================

export async function uploadResume(file: File): Promise<Resume> {
  const formData = new FormData();
  formData.append("file", file);
  return apiClient.post<Resume>("/resumes/", formData);
}

export async function listResumes(): Promise<ResumeList> {
  return apiClient.get<ResumeList>("/resumes/");
}

export async function deleteResume(resumeId: string): Promise<{ detail: string }> {
  return apiClient.delete<{ detail: string }>(`/resumes/${resumeId}`);
}

export async function getResume(resumeId: string): Promise<Resume> {
  return apiClient.get<Resume>(`/resumes/${resumeId}`);
}


// ============================================================================
// Job Endpoints
// ============================================================================

export async function createJob(title: string, description: string): Promise<JobDescription> {
  return apiClient.post<JobDescription>("/jobs/", { title, description });
}

export async function listJobs(): Promise<JobList> {
  return apiClient.get<JobList>("/jobs/");
}

export async function getJob(jobId: string): Promise<JobDescription> {
  return apiClient.get<JobDescription>(`/jobs/${jobId}`);
}

export async function deleteJob(jobId: string): Promise<{ detail: string }> {
  return apiClient.delete<{ detail: string }>(`/jobs/${jobId}`);
}

export async function calculateMatch(resumeId: string, jobId: string): Promise<MatchResult> {
  return apiClient.post<MatchResult>("/jobs/match", { resume_id: resumeId, job_id: jobId });
}


// ============================================================================
// Analysis Endpoints
// ============================================================================

export async function createAnalysis(resumeId: string, jobDescId?: string): Promise<Analysis> {
  return apiClient.post<Analysis>("/analyses/", {
    resume_id: resumeId,
    job_desc_id: jobDescId ?? null,
  });
}

export async function listAnalyses(): Promise<AnalysisList> {
  return apiClient.get<AnalysisList>("/analyses/");
}

export async function getAnalysis(analysisId: string): Promise<Analysis> {
  return apiClient.get<Analysis>(`/analyses/${analysisId}`);
}

export async function deleteAnalysis(analysisId: string): Promise<{ detail: string }> {
  return apiClient.delete<{ detail: string }>(`/analyses/${analysisId}`);
}