"use client";

import {
  ArrowPathIcon,
  ArrowRightIcon,
  BriefcaseIcon,
  ChartBarSquareIcon,
  CheckCircleIcon,
  DocumentArrowUpIcon,
  DocumentTextIcon,
  PlayIcon,
  PlusIcon,
  PowerIcon,
  XMarkIcon,
  SparklesIcon,
  ExclamationTriangleIcon,
  TrashIcon,
} from "@heroicons/react/24/outline";
import Link from "next/link";
import type { FormEvent, ReactNode } from "react";
import { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import type { Analysis, JobDescription, Resume } from "@/lib/api";
import {
  createAnalysis,
  createJob,
  deleteResume,
  getMe,
  listAnalyses,
  listJobs,
  listResumes,
  logout,
  uploadResume,
} from "@/lib/api";

type Tab = "resume" | "job" | "analyze" | "history";

const tabs: Array<{ id: Tab; label: string; icon: ReactNode }> = [
  { id: "resume", label: "Resume", icon: <DocumentArrowUpIcon className="w-5 h-5" /> },
  { id: "job", label: "Job", icon: <BriefcaseIcon className="w-5 h-5" /> },
  { id: "analyze", label: "Analyze", icon: <ChartBarSquareIcon className="w-5 h-5" /> },
  { id: "history", label: "History", icon: <DocumentTextIcon className="w-5 h-5" /> },
];

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Recently";
  return new Intl.DateTimeFormat("en", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(date);
}

function scoreTone(score?: number | null) {
  if (!score) return "text-gray-400";
  if (score >= 80) return "text-accent-emerald";
  if (score >= 60) return "text-accent-gold";
  return "text-red-400";
}

function ScoreGauge({ score }: { score: number }) {
  const circumference = 2 * Math.PI * 45;
  const progress = (score / 100) * circumference;
  
  return (
    <div className="relative w-32 h-32">
      <svg className="w-32 h-32 transform -rotate-90">
        <circle
          cx="64"
          cy="64"
          r="45"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="8"
          fill="none"
        />
        <circle
          cx="64"
          cy="64"
          r="45"
          stroke={score >= 80 ? "#10b981" : score >= 60 ? "#f59e0b" : "#ef4444"}
          strokeWidth="8"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          className="transition-all duration-1000"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className={`text-3xl font-bold ${scoreTone(score)}`}>{score}%</span>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<Tab>("resume");
  const [userEmail, setUserEmail] = useState("");
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [jobs, setJobs] = useState<JobDescription[]>([]);
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [selectedJobId, setSelectedJobId] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [currentAnalysis, setCurrentAnalysis] = useState<Analysis | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(false);
  const [deletingResumeId, setDeletingResumeId] = useState<string | null>(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState<string | null>(null);

  const visibleAnalysis = currentAnalysis ?? analyses[0] ?? null;

  const selectedResume = useMemo(
    () => resumes.find((resume) => resume.id === selectedResumeId),
    [resumes, selectedResumeId],
  );

  async function loadWorkspace() {
    setError("");
    try {
      const [me, resumeResult, jobResult, analysisResult] = await Promise.all([
        getMe(),
        listResumes(),
        listJobs(),
        listAnalyses(),
      ]);
      setUserEmail(me.email);
      setResumes(resumeResult.resumes);
      setJobs(jobResult.jobs);
      setAnalyses(analysisResult.analyses);
      setSelectedResumeId((current) => current || resumeResult.resumes[0]?.id || "");
      setSelectedJobId((current) => current || jobResult.jobs[0]?.id || "");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load the workspace.");
    }
  }

  useEffect(() => {
    void loadWorkspace();
  }, []);

  async function onUpload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) return;

    setLoading(true);
    setUploadProgress(true);
    setError("");
    setMessage("");
    try {
      const uploaded = await uploadResume(file);
      setResumes((items) => [uploaded, ...items]);
      setSelectedResumeId(uploaded.id);
      setFile(null);
      setMessage("Resume uploaded and parsed successfully.");
      setActiveTab("job");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not upload the resume.");
    } finally {
      setLoading(false);
      setUploadProgress(false);
    }
  }

  async function onDeleteResume(resumeId: string) {
    setDeletingResumeId(resumeId);
    setError("");
    try {
      await deleteResume(resumeId);
      setResumes((items) => items.filter((r) => r.id !== resumeId));
      setAnalyses((items) => items.filter((a) => a.resume_id !== resumeId));
      if (selectedResumeId === resumeId) {
        setSelectedResumeId("");
        setCurrentAnalysis(null);
      }
      setMessage("Resume deleted successfully.");
      setConfirmDeleteId(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not delete the resume.");
    } finally {
      setDeletingResumeId(null);
    }
  }

  async function onCreateJob(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    try {
      const job = await createJob(jobTitle, jobDescription);
      setJobs((items) => [job, ...items]);
      setSelectedJobId(job.id);
      setJobTitle("");
      setJobDescription("");
      setMessage("Job description saved.");
      setActiveTab("analyze");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save the job description.");
    } finally {
      setLoading(false);
    }
  }

  async function onAnalyze() {
    if (!selectedResumeId) {
      setError("Upload or select a resume first.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");
    try {
      const analysis = await createAnalysis(selectedResumeId, selectedJobId || undefined);
      setCurrentAnalysis(analysis);
      setAnalyses((items) => [analysis, ...items]);
      setMessage("Analysis complete!");
      setActiveTab("analyze");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not run the analysis.");
    } finally {
      setLoading(false);
    }
  }

  async function onLogout() {
    try {
      await logout();
    } finally {
      window.location.href = "/login";
    }
  }

  return (
    <main className="min-h-screen bg-surface-primary">
      {/* Header */}
      <header className="border-b border-border-subtle bg-surface-secondary/50 backdrop-blur-xl sticky top-0 z-40">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent-gold to-accent-goldDark flex items-center justify-center">
                <SparklesIcon className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold text-white">ResumeAI</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-accent-gold/20 flex items-center justify-center text-accent-gold text-sm font-medium">
                  {userEmail?.charAt(0).toUpperCase()}
                </div>
                <span className="text-sm text-gray-400 hidden sm:inline">{userEmail}</span>
              </div>
              <button
                className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-surface-tertiary transition-colors"
                onClick={() => void loadWorkspace()}
                title="Refresh"
              >
                <ArrowPathIcon className="w-5 h-5" />
              </button>
              <button
                className="p-2 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                onClick={() => void onLogout()}
                title="Logout"
              >
                <PowerIcon className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Notifications */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-6">
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-4 p-4 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center gap-3"
            >
              <ExclamationTriangleIcon className="w-5 h-5 text-red-400 flex-shrink-0" />
              <p className="text-red-400 text-sm">{error}</p>
              {error.toLowerCase().includes("authenticated") && (
                <Link className="ml-auto text-accent-gold hover:text-accent-goldLight font-medium text-sm" href="/login">
                  Login
                </Link>
              )}
            </motion.div>
          )}
          {message && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-4 p-4 rounded-xl bg-accent-emerald/10 border border-accent-emerald/20 flex items-center gap-3"
            >
              <CheckCircleIcon className="w-5 h-5 text-accent-emerald flex-shrink-0" />
              <p className="text-accent-emerald text-sm">{message}</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-[280px_1fr] gap-8">
          {/* Sidebar */}
          <aside className="space-y-6">
            <nav className="card-premium p-2">
              {tabs.map((tab) => (
                <button
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition-all ${
                    activeTab === tab.id
                      ? "bg-accent-gold/15 text-accent-gold"
                      : "text-gray-400 hover:text-white hover:bg-surface-tertiary"
                  }`}
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
            </nav>

            {/* Stats */}
            <div className="card-premium p-6">
              <h3 className="text-sm font-medium text-gray-500 mb-4">Your Stats</h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-white">{resumes.length}</div>
                  <div className="text-xs text-gray-500">Resumes</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-white">{jobs.length}</div>
                  <div className="text-xs text-gray-500">Jobs</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-white">{analyses.length}</div>
                  <div className="text-xs text-gray-500">Analyses</div>
                </div>
              </div>
            </div>
          </aside>

          {/* Content Area */}
          <div className="min-w-0">
            {activeTab === "resume" && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="card-premium p-8"
              >
                <div className="flex items-center gap-4 mb-8">
                  <div className="w-12 h-12 rounded-xl bg-accent-gold/20 flex items-center justify-center">
                    <DocumentArrowUpIcon className="w-6 h-6 text-accent-gold" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-white">Upload Resume</h2>
                    <p className="text-gray-500">PDF files up to 5 MB are accepted</p>
                  </div>
                </div>

                <form className="space-y-4" onSubmit={onUpload}>
                  <div className="border-2 border-dashed border-border-medium rounded-xl p-8 text-center hover:border-accent-gold/50 transition-colors">
                    <input
                      accept="application/pdf"
                      className="hidden"
                      id="file-upload"
                      onChange={(event) => setFile(event.target.files?.[0] ?? null)}
                      type="file"
                    />
                    <label htmlFor="file-upload" className="cursor-pointer">
                      {file ? (
                        <div className="flex items-center justify-center gap-3">
                          <DocumentTextIcon className="w-8 h-8 text-accent-gold" />
                          <span className="text-white font-medium">{file.name}</span>
                          <button
                            className="p-1 hover:bg-surface-tertiary rounded"
                            onClick={(e) => { e.preventDefault(); setFile(null); }}
                            type="button"
                          >
                            <XMarkIcon className="w-4 h-4 text-gray-400" />
                          </button>
                        </div>
                      ) : (
                        <>
                          <DocumentArrowUpIcon className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                          <p className="text-gray-400 mb-2">
                            Drag and drop your resume here, or <span className="text-accent-gold">browse</span>
                          </p>
                          <p className="text-gray-600 text-sm">PDF only, max 5MB</p>
                        </>
                      )}
                    </label>
                  </div>

                  <button
                    className="btn-primary w-full py-3.5"
                    disabled={!file || loading}
                    type="submit"
                  >
                    {loading || uploadProgress ? (
                      <>
                        <span className="animate-spin mr-2">⏳</span>
                        Processing...
                      </>
                    ) : (
                      <>
                        <DocumentArrowUpIcon className="w-5 h-5" />
                        Upload Resume
                      </>
                    )}
                  </button>
                </form>

                {resumes.length > 0 && (
                  <div className="mt-8">
                    <h3 className="text-sm font-medium text-gray-500 mb-4">Your Resumes</h3>
                    <div className="space-y-2">
                      {resumes.map((resume) => (
                        <div
                          className={`group flex items-center justify-between p-4 rounded-xl border transition-all cursor-pointer ${
                            selectedResumeId === resume.id
                              ? "bg-accent-gold/10 border-accent-gold/30"
                              : "bg-surface-secondary border-border-subtle hover:border-border-medium"
                          }`}
                          key={resume.id}
                          onClick={() => setSelectedResumeId(resume.id)}
                        >
                          <div className="flex items-center gap-3">
                            <DocumentTextIcon className="w-5 h-5 text-gray-400" />
                            <span className="text-white font-medium">{resume.filename}</span>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="text-gray-500 text-sm">{formatDate(resume.uploaded_at)}</span>
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                setConfirmDeleteId(resume.id);
                              }}
                              className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 rounded-lg transition-all"
                              title="Delete resume"
                            >
                              <TrashIcon className="w-4 h-4 text-red-400" />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {activeTab === "job" && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="card-premium p-8"
              >
                <div className="flex items-center gap-4 mb-8">
                  <div className="w-12 h-12 rounded-xl bg-accent-violet/20 flex items-center justify-center">
                    <BriefcaseIcon className="w-6 h-6 text-accent-violet" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-white">Target Job</h2>
                    <p className="text-gray-500">Save a role to compare against your resume</p>
                  </div>
                </div>

                <form className="space-y-5" onSubmit={onCreateJob}>
                  <div>
                    <label className="label-premium">Job Title</label>
                    <input
                      className="input-premium"
                      placeholder="e.g. Senior Software Engineer"
                      value={jobTitle}
                      onChange={(event) => setJobTitle(event.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <label className="label-premium">Job Description</label>
                    <textarea
                      className="input-premium min-h-[200px]"
                      placeholder="Paste the job description here..."
                      value={jobDescription}
                      onChange={(event) => setJobDescription(event.target.value)}
                      required
                    />
                  </div>
                  <button
                    className="btn-primary w-full py-3.5"
                    disabled={loading}
                    type="submit"
                  >
                    <PlusIcon className="w-5 h-5" />
                    Save Job Description
                  </button>
                </form>

                {jobs.length > 0 && (
                  <div className="mt-8">
                    <h3 className="text-sm font-medium text-gray-500 mb-4">Saved Jobs</h3>
                    <div className="space-y-2">
                      {jobs.map((job) => (
                        <button
                          className={`w-full flex items-center justify-between p-4 rounded-xl border transition-all ${
                            selectedJobId === job.id
                              ? "bg-accent-violet/10 border-accent-violet/30"
                              : "bg-surface-secondary border-border-subtle hover:border-border-medium"
                          }`}
                          key={job.id}
                          onClick={() => setSelectedJobId(job.id)}
                          type="button"
                        >
                          <div className="flex items-center gap-3">
                            <BriefcaseIcon className="w-5 h-5 text-gray-400" />
                            <span className="text-white font-medium">{job.title}</span>
                          </div>
                          <span className="text-gray-500 text-sm">{formatDate(job.uploaded_at)}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {activeTab === "analyze" && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="grid lg:grid-cols-[1fr_1fr] gap-8"
              >
                <div className="card-premium p-8">
                  <div className="flex items-center gap-4 mb-8">
                    <div className="w-12 h-12 rounded-xl bg-accent-emerald/20 flex items-center justify-center">
                      <PlayIcon className="w-6 h-6 text-accent-emerald" />
                    </div>
                    <div>
                      <h2 className="text-xl font-bold text-white">Run Analysis</h2>
                      <p className="text-gray-500">Select resume and optional target job</p>
                    </div>
                  </div>

                  <div className="space-y-5">
                    <div>
                      <label className="label-premium">Resume</label>
                      <select
                        className="input-premium"
                        value={selectedResumeId}
                        onChange={(event) => setSelectedResumeId(event.target.value)}
                      >
                        <option value="">Select a resume</option>
                        {resumes.map((resume) => (
                          <option key={resume.id} value={resume.id}>
                            {resume.filename}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="label-premium">Target Job (Optional)</label>
                      <select
                        className="input-premium"
                        value={selectedJobId}
                        onChange={(event) => setSelectedJobId(event.target.value)}
                      >
                        <option value="">No target job</option>
                        {jobs.map((job) => (
                          <option key={job.id} value={job.id}>
                            {job.title}
                          </option>
                        ))}
                      </select>
                    </div>
                    <button
                      className="btn-primary w-full py-3.5"
                      disabled={!selectedResumeId || loading}
                      onClick={() => void onAnalyze()}
                      type="button"
                    >
                      {loading ? (
                        <>
                          <span className="animate-spin mr-2">⏳</span>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <ChartBarSquareIcon className="w-5 h-5" />
                          Analyze Resume
                        </>
                      )}
                    </button>
                  </div>
                </div>

                <AnalysisPanel analysis={visibleAnalysis} resumeName={selectedResume?.filename} />
              </motion.div>
            )}

            {activeTab === "history" && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="card-premium p-8"
              >
                <div className="flex items-center gap-4 mb-8">
                  <div className="w-12 h-12 rounded-xl bg-accent-gold/20 flex items-center justify-center">
                    <DocumentTextIcon className="w-6 h-6 text-accent-gold" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-white">Analysis History</h2>
                    <p className="text-gray-500">Previous ATS scores and recommendations</p>
                  </div>
                </div>

                {analyses.length > 0 ? (
                  <div className="space-y-3">
                    {analyses.map((analysis) => {
                      const score = analysis.overall_score ?? analysis.ats_score ?? 0;
                      const level = analysis.seniority_classification?.level;
                      return (
                        <Link
                          href={`/analysis/${analysis.id}`}
                          className="w-full flex items-center justify-between p-5 rounded-xl bg-surface-secondary border border-border-subtle hover:border-border-medium transition-all block"
                          key={analysis.id}
                        >
                          <div className="flex items-center gap-4">
                            <ScoreGauge score={score} />
                            <div className="text-left">
                              <div className="font-medium text-white">
                                {score}% Overall Score
                              </div>
                              {level && (
                                <div className="text-sm text-amber-400">
                                  {level}
                                </div>
                              )}
                              <div className="text-sm text-gray-500">{formatDate(analysis.created_at)}</div>
                            </div>
                          </div>
                          <ArrowRightIcon className="w-5 h-5 text-gray-500" />
                        </Link>
                      );
                    })}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <DocumentTextIcon className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <p className="text-gray-500">No analyses yet</p>
                    <p className="text-gray-600 text-sm">Upload a resume and run an analysis to see results here</p>
                  </div>
                )}
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}

function AnalysisPanel({ analysis, resumeName }: { analysis: Analysis | null; resumeName?: string }) {
  if (!analysis) {
    return (
      <div className="card-premium p-8 flex flex-col items-center justify-center min-h-[400px] text-center">
        <div className="w-20 h-20 rounded-full bg-surface-tertiary flex items-center justify-center mb-6">
          <ChartBarSquareIcon className="w-10 h-10 text-gray-600" />
        </div>
        <h3 className="text-xl font-bold text-white mb-2">No analysis selected</h3>
        <p className="text-gray-500 max-w-sm">
          Choose a resume and run an analysis to see your ATS score and recommendations here.
        </p>
      </div>
    );
  }

  const score = analysis.overall_score ?? analysis.ats_score ?? 0;
  const matched = analysis.keyword_analysis?.exact_matches ?? [];
  const missing = analysis.missing_skills?.technologies ?? analysis.keyword_analysis?.missing_critical ?? [];
  const suggestions = analysis.score_categories?.[0]?.recommendations ?? analysis.suggestions ?? [];
  const bullets = analysis.improved_bullets?.map(b => b.improved) ?? analysis.rewritten_bullets ?? [];
  const level = analysis.seniority_classification?.level;
  const strengths = analysis.seniority_classification?.strengths ?? [];
  const weaknesses = analysis.seniority_classification?.weaknesses ?? [];

  return (
    <div className="card-premium p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <p className="text-sm text-gray-500">{resumeName || "Selected resume"}</p>
          <h3 className="text-xl font-bold text-white">Analysis Results</h3>
          {level && (
            <span className="inline-block mt-1 px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 text-xs">
              {level}
            </span>
          )}
        </div>
        <ScoreGauge score={score} />
      </div>

      <div className="space-y-6">
        {strengths.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Key Strengths</h4>
            <div className="flex flex-wrap gap-2">
              {strengths.map((s, i) => (
                <span key={i} className="badge-emerald">{s}</span>
              ))}
            </div>
          </div>
        )}

        {weaknesses.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Areas to Improve</h4>
            <div className="flex flex-wrap gap-2">
              {weaknesses.map((w, i) => (
                <span key={i} className="badge-gold">{w}</span>
              ))}
            </div>
          </div>
        )}

        {matched.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Matched Keywords ({matched.length})</h4>
            <div className="flex flex-wrap gap-2">
              {matched.slice(0, 10).map((keyword, i) => (
                <span key={i} className="badge-emerald">{keyword}</span>
              ))}
              {matched.length > 10 && (
                <span className="text-gray-500 text-xs">+{matched.length - 10} more</span>
              )}
            </div>
          </div>
        )}

        {missing.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Missing/Recommended Skills</h4>
            <div className="flex flex-wrap gap-2">
              {missing.slice(0, 8).map((keyword, i) => (
                <span key={i} className="badge-gold">{keyword}</span>
              ))}
            </div>
          </div>
        )}

        {bullets.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">AI-Generated Improvements</h4>
            <ul className="space-y-2">
              {bullets.slice(0, 3).map((bullet, index) => (
                <li key={index} className="p-3 rounded-lg bg-surface-secondary border border-border-subtle text-gray-300 text-sm">
                  {bullet}
                </li>
              ))}
            </ul>
          </div>
        )}

        <Link
          href={`/analysis/${analysis.id}`}
          className="btn-secondary w-full py-3 flex items-center justify-center gap-2"
        >
          <ChartBarSquareIcon className="w-5 h-5" />
          View Full Analysis
        </Link>

        {matched.length === 0 && missing.length === 0 && suggestions.length === 0 && bullets.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500">Analysis complete. Results will appear here.</p>
          </div>
        )}
      </div>
        
    </div>
  );
}
