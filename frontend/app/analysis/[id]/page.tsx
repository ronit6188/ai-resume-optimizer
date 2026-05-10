"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowLeftIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  StarIcon,
  ChartBarIcon,
  DocumentTextIcon,
  UserIcon,
  LightBulbIcon,
  RocketLaunchIcon,
  CodeBracketIcon,
  AcademicCapIcon,
} from "@heroicons/react/24/outline";
import type { Analysis } from "@/lib/api";
import { getAnalysis } from "@/lib/api";

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

export default function AnalysisDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    async function loadAnalysis() {
      try {
        const data = await getAnalysis(params.id as string);
        setAnalysis(data);
      } catch (error) {
        console.error("Failed to load analysis:", error);
      } finally {
        setLoading(false);
      }
    }
    loadAnalysis();
  }, [params.id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-gray-400">Loading analysis...</p>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-400 mb-4">Analysis not found</p>
          <Link href="/dashboard" className="text-amber-500 hover:text-amber-400">
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: "overview", label: "Overview", icon: ChartBarIcon },
    { id: "scores", label: "Detailed Scores", icon: StarIcon },
    { id: "technical", label: "Technical Analysis", icon: CodeBracketIcon },
    { id: "recruiter", label: "Recruiter View", icon: UserIcon },
    { id: "improvements", label: "Improvements", icon: LightBulbIcon },
    { id: "career", label: "Career Path", icon: RocketLaunchIcon },
  ];

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      {/* Header */}
      <div className="border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push("/dashboard")}
              className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              <ArrowLeftIcon className="w-5 h-5 text-gray-400" />
            </button>
            <div>
              <h1 className="text-xl font-bold">Analysis Results</h1>
              <p className="text-sm text-gray-400">
                {new Date(analysis.created_at).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Score Banner */}
      <div className="bg-gradient-to-r from-amber-900/20 via-amber-800/10 to-amber-900/20 border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center gap-8">
            {/* Overall Score Circle */}
            <div className="relative">
              <svg className="w-32 h-32" viewBox="0 0 120 120">
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  fill="none"
                  stroke="white/10"
                  strokeWidth="8"
                />
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  fill="none"
                  stroke="url(#goldGradient)"
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={`${(analysis.overall_score || 0) * 3.39} 339`}
                  transform="rotate(-90 60 60)"
                />
                <defs>
                  <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#f59e0b" />
                    <stop offset="100%" stopColor="#d97706" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-4xl font-bold text-amber-500">
                  {analysis.overall_score || 0}
                </span>
              </div>
            </div>

            {/* Seniority Badge */}
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <span className="px-3 py-1 rounded-full bg-amber-500/20 text-amber-500 text-sm font-medium">
                  {analysis.seniority_classification?.level || "Unknown Level"}
                </span>
                <span className="text-gray-400 text-sm">
                  Confidence: {Math.round(analysis.seniority_classification?.confidence_score || 0)}%
                </span>
              </div>
              <p className="text-gray-300 text-sm leading-relaxed max-w-2xl">
                {analysis.seniority_classification?.explanation}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="border-b border-white/10 bg-white/5">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex gap-1 overflow-x-auto py-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
                  activeTab === tab.id
                    ? "bg-amber-500/20 text-amber-500"
                    : "text-gray-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Tab Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === "overview" && (
          <OverviewTab analysis={analysis} />
        )}
        {activeTab === "scores" && (
          <ScoresTab analysis={analysis} />
        )}
        {activeTab === "technical" && (
          <TechnicalTab analysis={analysis} />
        )}
        {activeTab === "recruiter" && (
          <RecruiterTab analysis={analysis} />
        )}
        {activeTab === "improvements" && (
          <ImprovementsTab analysis={analysis} />
        )}
        {activeTab === "career" && (
          <CareerTab analysis={analysis} />
        )}
      </div>
    </div>
  );
}

function OverviewTab({ analysis }: { analysis: Analysis }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Key Metrics */}
      {analysis.score_categories?.slice(0, 6).map((category, index) => (
        <motion.div
          key={category.name}
          variants={fadeIn}
          initial="initial"
          animate="animate"
          transition={{ delay: index * 0.1 }}
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-400 text-sm">{category.name}</h3>
            <span className="text-2xl font-bold text-amber-500">
              {category.score}/{category.max_score}
            </span>
          </div>
          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-amber-500 to-amber-600 rounded-full"
              style={{ width: `${(category.score / category.max_score) * 100}%` }}
            />
          </div>
        </motion.div>
      ))}

      {/* Strengths */}
      {analysis.seniority_classification?.strengths && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6 md:col-span-2"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <CheckCircleIcon className="w-5 h-5 text-green-500" />
            Key Strengths
          </h3>
          <div className="flex flex-wrap gap-2">
            {analysis.seniority_classification.strengths.map((strength, i) => (
              <span
                key={i}
                className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm"
              >
                {strength}
              </span>
            ))}
          </div>
        </motion.div>
      )}

      {/* Weaknesses */}
      {analysis.seniority_classification?.weaknesses && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <ExclamationTriangleIcon className="w-5 h-5 text-amber-500" />
            Areas to Improve
          </h3>
          <ul className="space-y-2">
            {analysis.seniority_classification.weaknesses.map((weakness, i) => (
              <li key={i} className="text-gray-400 text-sm flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-amber-500 rounded-full" />
                {weakness}
              </li>
            ))}
          </ul>
        </motion.div>
      )}
    </div>
  );
}

function ScoresTab({ analysis }: { analysis: Analysis }) {
  return (
    <div className="space-y-6">
      {analysis.score_categories?.map((category, index) => (
        <motion.div
          key={category.name}
          variants={fadeIn}
          initial="initial"
          animate="animate"
          transition={{ delay: index * 0.1 }}
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">{category.name}</h3>
            <div className="flex items-center gap-3">
              <span className="text-3xl font-bold text-amber-500">
                {category.score}
              </span>
              <span className="text-gray-400">/ {category.max_score}</span>
            </div>
          </div>
          
          <div className="h-3 bg-white/10 rounded-full overflow-hidden mb-4">
            <div
              className="h-full bg-gradient-to-r from-amber-500 to-amber-600 rounded-full transition-all duration-500"
              style={{ width: `${(category.score / category.max_score) * 100}%` }}
            />
          </div>

          {category.details.length > 0 && (
            <div className="mb-4">
              <h4 className="text-sm text-gray-400 mb-2">Analysis Details:</h4>
              <ul className="space-y-1">
                {category.details.slice(0, 3).map((detail, i) => (
                  <li key={i} className="text-gray-300 text-sm flex items-center gap-2">
                    <CheckCircleIcon className="w-4 h-4 text-green-500" />
                    {detail}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {category.recommendations.length > 0 && (
            <div className="pt-4 border-t border-white/10">
              <h4 className="text-sm text-gray-400 mb-2">Recommendations:</h4>
              <ul className="space-y-1">
                {category.recommendations.slice(0, 3).map((rec, i) => (
                  <li key={i} className="text-amber-400 text-sm flex items-center gap-2">
                    <span className="text-amber-500">→</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </motion.div>
      ))}
    </div>
  );
}

function TechnicalTab({ analysis }: { analysis: Analysis }) {
  const tech = analysis.technical_analysis;
  const keywords = analysis.keyword_analysis;
  const structure = analysis.resume_structure;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Technical Stack */}
      {tech && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <CodeBracketIcon className="w-5 h-5 text-amber-500" />
            Technical Stack
          </h3>
          <p className="text-sm text-gray-400 mb-4">
            Maturity Level: <span className="text-amber-500 font-medium">{tech.maturity_level}</span>
          </p>

          <div className="space-y-4">
            {tech.programming_languages.length > 0 && (
              <div>
                <h4 className="text-sm text-gray-400 mb-2">Languages</h4>
                <div className="flex flex-wrap gap-2">
                  {tech.programming_languages.map((lang, i) => (
                    <span key={i} className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm">
                      {lang}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {tech.frameworks.length > 0 && (
              <div>
                <h4 className="text-sm text-gray-400 mb-2">Frameworks</h4>
                <div className="flex flex-wrap gap-2">
                  {tech.frameworks.map((fw, i) => (
                    <span key={i} className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-full text-sm">
                      {fw}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {tech.databases.length > 0 && (
              <div>
                <h4 className="text-sm text-gray-400 mb-2">Databases</h4>
                <div className="flex flex-wrap gap-2">
                  {tech.databases.map((db, i) => (
                    <span key={i} className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                      {db}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {tech.cloud_devops.length > 0 && (
              <div>
                <h4 className="text-sm text-gray-400 mb-2">Cloud & DevOps</h4>
                <div className="flex flex-wrap gap-2">
                  {tech.cloud_devops.map((cd, i) => (
                    <span key={i} className="px-3 py-1 bg-orange-500/20 text-orange-400 rounded-full text-sm">
                      {cd}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {tech.ai_ml_tools.length > 0 && (
              <div>
                <h4 className="text-sm text-gray-400 mb-2">AI/ML Tools</h4>
                <div className="flex flex-wrap gap-2">
                  {tech.ai_ml_tools.map((ml, i) => (
                    <span key={i} className="px-3 py-1 bg-pink-500/20 text-pink-400 rounded-full text-sm">
                      {ml}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Keywords Analysis */}
      {keywords && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Keyword Analysis</h3>
          
          <div className="mb-4">
            <div className="text-3xl font-bold text-amber-500 mb-1">
              {keywords.match_percentage}%
            </div>
            <p className="text-gray-400 text-sm">Keyword Match Rate</p>
          </div>

          {keywords.exact_matches.length > 0 && (
            <div className="mb-4">
              <h4 className="text-sm text-gray-400 mb-2">Matched Keywords</h4>
              <div className="flex flex-wrap gap-2">
                {keywords.exact_matches.slice(0, 10).map((kw, i) => (
                  <span key={i} className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {keywords.missing_critical.length > 0 && (
            <div>
              <h4 className="text-sm text-gray-400 mb-2">Missing Keywords</h4>
              <div className="flex flex-wrap gap-2">
                {keywords.missing_critical.slice(0, 10).map((kw, i) => (
                  <span key={i} className="px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs">
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Resume Structure */}
      {structure && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <DocumentTextIcon className="w-5 h-5 text-amber-500" />
            Resume Structure
          </h3>
          
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className={`p-3 rounded-lg ${structure.has_contact_info ? "bg-green-500/20" : "bg-red-500/20"}`}>
              <span className="text-sm text-gray-400">Contact Info</span>
              <p className={structure.has_contact_info ? "text-green-400" : "text-red-400"}>
                {structure.has_contact_info ? "Present" : "Missing"}
              </p>
            </div>
            <div className={`p-3 rounded-lg ${structure.has_summary ? "bg-green-500/20" : "bg-red-500/20"}`}>
              <span className="text-sm text-gray-400">Summary</span>
              <p className={structure.has_summary ? "text-green-400" : "text-red-400"}>
                {structure.has_summary ? "Present" : "Missing"}
              </p>
            </div>
            <div className={`p-3 rounded-lg ${structure.has_experience ? "bg-green-500/20" : "bg-red-500/20"}`}>
              <span className="text-sm text-gray-400">Experience</span>
              <p className={structure.has_experience ? "text-green-400" : "text-red-400"}>
                {structure.has_experience ? "Present" : "Missing"}
              </p>
            </div>
            <div className={`p-3 rounded-lg ${structure.has_skills ? "bg-green-500/20" : "bg-red-500/20"}`}>
              <span className="text-sm text-gray-400">Skills</span>
              <p className={structure.has_skills ? "text-green-400" : "text-red-400"}>
                {structure.has_skills ? "Present" : "Missing"}
              </p>
            </div>
          </div>

          <p className="text-gray-400 text-sm">
            {structure.section_count} sections detected | Readability: {structure.readability_score}%
          </p>

          {structure.formatting_issues.length > 0 && (
            <div className="mt-4 pt-4 border-t border-white/10">
              <h4 className="text-sm text-gray-400 mb-2">Formatting Issues</h4>
              <ul className="space-y-1">
                {structure.formatting_issues.map((issue, i) => (
                  <li key={i} className="text-amber-400 text-sm flex items-center gap-2">
                    <span className="text-amber-500">!</span>
                    {issue}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </motion.div>
      )}

      {/* Experience Quality */}
      {analysis.experience_quality && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Experience Quality</h3>
          
          <div className="mb-4">
            <div className="text-3xl font-bold text-amber-500 mb-1">
              {analysis.experience_quality.quality_score}
            </div>
            <p className="text-gray-400 text-sm">Quality Score</p>
          </div>

          {analysis.experience_quality.measurable_achievements.length > 0 && (
            <div className="mb-4">
              <h4 className="text-sm text-gray-400 mb-2">Quantifiable Achievements</h4>
              <div className="flex flex-wrap gap-2">
                {analysis.experience_quality.measurable_achievements.slice(0, 5).map((a, i) => (
                  <span key={i} className="px-2 py-1 bg-amber-500/20 text-amber-400 rounded text-xs">
                    {a}
                  </span>
                ))}
              </div>
            </div>
          )}

          {analysis.experience_quality.leadership_indicators.length > 0 && (
            <div>
              <h4 className="text-sm text-gray-400 mb-2">Leadership Indicators</h4>
              <div className="flex flex-wrap gap-2">
                {analysis.experience_quality.leadership_indicators.map((li, i) => (
                  <span key={i} className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">
                    {li}
                  </span>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}

function RecruiterTab({ analysis }: { analysis: Analysis }) {
  const recruiter = analysis.recruiter_simulation;

  if (!recruiter) {
    return <p className="text-gray-400">No recruiter simulation data available</p>;
  }

  return (
    <div className="space-y-6">
      {/* First Impression */}
      <motion.div
        variants={fadeIn}
        initial="initial"
        animate="animate"
        className="bg-gradient-to-r from-amber-900/20 to-amber-800/10 border border-amber-500/20 rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold mb-4">First Impression</h3>
        <p className="text-gray-300">{recruiter.first_impression}</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Strengths */}
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <CheckCircleIcon className="w-5 h-5 text-green-500" />
            What Recruiters Like
          </h3>
          <ul className="space-y-3">
            {recruiter.strengths.map((s, i) => (
              <li key={i} className="text-gray-300 flex items-start gap-2">
                <CheckCircleIcon className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                {s}
              </li>
            ))}
          </ul>
        </motion.div>

        {/* Red Flags */}
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <ExclamationTriangleIcon className="w-5 h-5 text-red-500" />
            Red Flags
          </h3>
          <ul className="space-y-3">
            {recruiter.red_flags.length > 0 ? (
              recruiter.red_flags.map((r, i) => (
                <li key={i} className="text-gray-300 flex items-start gap-2">
                  <ExclamationTriangleIcon className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                  {r}
                </li>
              ))
            ) : (
              <li className="text-green-400 flex items-center gap-2">
                <CheckCircleIcon className="w-5 h-5" />
                No red flags detected
              </li>
            )}
          </ul>
        </motion.div>

        {/* Missing Info */}
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Missing Information</h3>
          {recruiter.missing_information.length > 0 ? (
            <ul className="space-y-2">
              {recruiter.missing_information.map((m, i) => (
                <li key={i} className="text-amber-400 text-sm flex items-center gap-2">
                  <span className="text-amber-500">→</span>
                  {m}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-green-400">All key sections present</p>
          )}
        </motion.div>

        {/* Quick Notes */}
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Recruiter Notes</h3>
          <p className="text-gray-400 text-sm">{recruiter.quick_notes}</p>
        </motion.div>
      </div>

      {/* Verdict */}
      <motion.div
        variants={fadeIn}
        initial="initial"
        animate="animate"
        className="bg-white/5 border border-white/10 rounded-xl p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="text-center p-4 bg-amber-500/10 rounded-lg">
            <p className="text-gray-400 text-sm mb-2">Hiring Likelihood</p>
            <p className="text-2xl font-bold text-amber-500">{recruiter.hiring_likelihood}</p>
          </div>
          <div className="text-center p-4 bg-green-500/10 rounded-lg">
            <p className="text-gray-400 text-sm mb-2">Interview Probability</p>
            <p className="text-2xl font-bold text-green-500">{recruiter.interview_probability}</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

function ImprovementsTab({ analysis }: { analysis: Analysis }) {
  const improvements = analysis.improved_bullets;

  if (!improvements || improvements.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">No improvements available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {improvements.map((item, index) => (
        <motion.div
          key={index}
          variants={fadeIn}
          initial="initial"
          animate="animate"
          transition={{ delay: index * 0.1 }}
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 font-bold">
              {index + 1}
            </div>
            <div className="flex-1">
              <div className="mb-4">
                <p className="text-sm text-gray-400 mb-1">Original</p>
                <p className="text-gray-300">{item.original}</p>
              </div>
              <div className="mb-4 p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                <p className="text-sm text-green-400 mb-1">Improved</p>
                <p className="text-green-300 font-medium">{item.improved}</p>
              </div>
              <p className="text-sm text-gray-500">{item.explanation}</p>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

function CareerTab({ analysis }: { analysis: Analysis }) {
  const guidance = analysis.career_guidance;
  const missing = analysis.missing_skills;

  if (!guidance) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">No career guidance available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Next Level Requirements */}
      {analysis.seniority_classification?.next_level_requirements && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-gradient-to-r from-amber-900/20 to-amber-800/10 border border-amber-500/20 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <RocketLaunchIcon className="w-5 h-5 text-amber-500" />
            Path to Next Level
          </h3>
          <p className="text-gray-300 mb-4">
            To reach the next seniority level, focus on:
          </p>
          <ul className="space-y-2">
            {analysis.seniority_classification.next_level_requirements.map((req, i) => (
              <li key={i} className="flex items-center gap-3">
                <span className="w-6 h-6 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 text-sm">
                  {i + 1}
                </span>
                <span className="text-gray-300">{req}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      )}

      {/* Roadmap */}
      {guidance.roadmap_to_next_level && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Career Roadmap</h3>
          <div className="space-y-4">
            {guidance.roadmap_to_next_level.map((item, i) => (
              <div key={i} className="flex gap-4">
                <div className="flex-shrink-0 w-24 text-amber-500 font-medium">
                  {item.phase}
                </div>
                <div className="flex-1 text-gray-300">
                  {item.action}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Missing Skills */}
        {missing && (
          <motion.div
            variants={fadeIn}
            initial="initial"
            animate="animate"
            className="bg-white/5 border border-white/10 rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold mb-4">Missing Skills</h3>
            
            {missing.technologies.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm text-gray-400 mb-2">Technologies to Learn</h4>
                <div className="flex flex-wrap gap-2">
                  {missing.technologies.map((t, i) => (
                    <span key={i} className="px-3 py-1 bg-red-500/20 text-red-400 rounded-full text-sm">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {missing.leadership_gaps.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm text-gray-400 mb-2">Leadership Gaps</h4>
                <ul className="space-y-1">
                  {missing.leadership_gaps.map((g, i) => (
                    <li key={i} className="text-amber-400 text-sm flex items-center gap-2">
                      <span className="text-amber-500">→</span>
                      {g}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {missing.experience_gaps.length > 0 && (
              <div>
                <h4 className="text-sm text-gray-400 mb-2">Experience Gaps</h4>
                <ul className="space-y-1">
                  {missing.experience_gaps.map((g, i) => (
                    <li key={i} className="text-amber-400 text-sm flex items-center gap-2">
                      <span className="text-amber-500">→</span>
                      {g}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}

        {/* Recommended Certifications */}
        {guidance.recommended_certifications && (
          <motion.div
            variants={fadeIn}
            initial="initial"
            animate="animate"
            className="bg-white/5 border border-white/10 rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <AcademicCapIcon className="w-5 h-5 text-amber-500" />
              Recommended Certifications
            </h3>
            <ul className="space-y-2">
              {guidance.recommended_certifications.map((cert, i) => (
                <li key={i} className="text-gray-300 flex items-center gap-2">
                  <span className="w-6 h-6 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 text-xs">
                    {i + 1}
                  </span>
                  {cert}
                </li>
              ))}
            </ul>
          </motion.div>
        )}

        {/* Recommended Projects */}
        {guidance.recommended_projects && (
          <motion.div
            variants={fadeIn}
            initial="initial"
            animate="animate"
            className="bg-white/5 border border-white/10 rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold mb-4">Recommended Projects</h3>
            <div className="space-y-4">
              {guidance.recommended_projects.map((project, i) => (
                <div key={i} className="p-4 bg-white/5 rounded-lg">
                  <h4 className="text-amber-500 font-medium mb-1">{project.title}</h4>
                  <p className="text-gray-400 text-sm">{project.description}</p>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Suggested Technologies */}
        {guidance.suggested_technologies && (
          <motion.div
            variants={fadeIn}
            initial="initial"
            animate="animate"
            className="bg-white/5 border border-white/10 rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold mb-4">Suggested Technologies</h3>
            <div className="flex flex-wrap gap-2">
              {guidance.suggested_technologies.map((tech, i) => (
                <span key={i} className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm">
                  {tech}
                </span>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* Improvement Priorities */}
      {guidance.improvement_priorities && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="bg-white/5 border border-white/10 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Improvement Priorities</h3>
          <div className="space-y-3">
            {guidance.improvement_priorities.map((item, i) => (
              <div key={i} className="flex items-center gap-4">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  item.priority === "High" 
                    ? "bg-red-500/20 text-red-400"
                    : item.priority === "Medium"
                    ? "bg-amber-500/20 text-amber-400"
                    : "bg-green-500/20 text-green-400"
                }`}>
                  {item.priority}
                </span>
                <span className="text-gray-300">{item.area}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}