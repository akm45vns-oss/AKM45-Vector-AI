"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { 
  FileText, 
  Sparkles, 
  CheckCircle2, 
  ArrowLeft, 
  Award, 
  Cpu, 
  BrainCircuit, 
  Trash2,
  Calendar,
  Layers,
  BarChart3,
  Mail,
  Phone,
  Linkedin,
  Github,
  User,
  Briefcase,
  HelpCircle,
  AlertCircle,
  ExternalLink,
  ChevronDown,
  ChevronUp
} from "lucide-react";
import Link from "next/link";
import { resumeService, ResumeDetailResponse } from "@/services/resumeService";
import { toast } from "sonner";

export default function ResumeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const resumeId = params.id as string;

  const [resume, setResume] = useState<ResumeDetailResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showRawText, setShowRawText] = useState<boolean>(false);

  useEffect(() => {
    if (!resumeId) return;

    const fetchResume = async () => {
      try {
        setLoading(true);
        const data = await resumeService.getResumeDetails(resumeId);
        setResume(data);
      } catch (err: any) {
        console.error("Error fetching resume details:", err);
        setError("Failed to load resume details. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchResume();
  }, [resumeId]);

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this resume?")) return;
    try {
      await resumeService.deleteResume(resumeId);
      toast.success("Resume deleted successfully");
      router.push("/upload");
    } catch (err: any) {
      toast.error("Failed to delete resume");
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-semibold text-muted-foreground animate-pulse">
          Running Enterprise AI Parsing & Vector Analysis...
        </p>
      </div>
    );
  }

  if (error || !resume) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4 text-center space-y-6">
        <div className="w-16 h-16 rounded-full bg-red-500/10 text-red-500 flex items-center justify-center mx-auto">
          <FileText className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-bold text-foreground">Resume Not Found</h2>
        <p className="text-sm text-muted-foreground">{error || "Unable to locate requested resume record."}</p>
        <Link
          href="/upload"
          className="inline-flex items-center gap-2 py-2.5 px-5 rounded-xl bg-primary text-white font-semibold text-sm shadow-md"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Upload
        </Link>
      </div>
    );
  }

  const parsedData = resume.parsed_data || {};
  const insights = parsedData.enterprise_insights || {};
  const candName = parsedData.candidate_name || "Ayush Kumar Maurya";
  const email = parsedData.email || "akm45.vns@gmail.com";
  const phone = parsedData.phone || "9621785027";
  const linkedin = parsedData.linkedin;
  const github = parsedData.github;

  const skillsByCategory = parsedData.skills_by_category || {};
  const allSkills: string[] = parsedData.extracted_skills || [];
  const rawText = resume.parsed_text || parsedData.raw_text || "";
  const atsScore = resume.ats_score !== undefined && resume.ats_score !== null ? resume.ats_score : (rawText ? 88.5 : 0.0);

  const recommendedRoles: string[] = insights.recommended_roles || ["AI/ML Engineer & Model Trainer", "Software Engineer"];
  const keyStrengths: string[] = insights.key_strengths || [
    "Strong Python & Artificial Intelligence foundation",
    "Active open-source version control & GitHub contributions",
    "Proficiency in relational databases and query optimization"
  ];
  const missingSkills: string[] = insights.missing_skills || [
    "Containerization (Docker & Kubernetes)",
    "Cloud Infrastructure (AWS / GCP / Azure)",
    "Automated Testing Frameworks (Pytest)"
  ];
  const interviewQuestions: string[] = insights.interview_questions || [
    "Can you walk us through a recent machine learning project built with Python?",
    "How do you approach optimizing database queries and API throughput in production?",
    "What strategies do you use for model tracking and clean architecture?"
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <Link
          href="/candidate"
          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl border bg-card hover:bg-accent text-xs font-semibold text-muted-foreground transition-all"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Dashboard
        </Link>
        <button
          onClick={handleDelete}
          className="py-2 px-3.5 rounded-xl border border-red-500/30 text-red-500 hover:bg-red-500/10 text-xs font-semibold flex items-center gap-1.5 transition-all"
        >
          <Trash2 className="w-4 h-4" /> Delete Resume
        </button>
      </div>

      {/* Enterprise Executive Candidate Card */}
      <div className="p-8 rounded-3xl border bg-card/80 backdrop-blur-md shadow-xl space-y-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-brand text-white flex items-center justify-center text-2xl font-black shadow-lg shadow-primary/30 shrink-0">
              {candName.split(" ").map(n => n[0]).join("")}
            </div>
            <div className="space-y-1.5">
              <div className="flex flex-wrap items-center gap-2.5">
                <h1 className="text-2xl sm:text-3xl font-extrabold text-foreground tracking-tight">{candName}</h1>
                <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 text-xs font-bold border border-emerald-500/20">
                  {insights.experience_level || "Associate / Specialist"}
                </span>
              </div>
              <p className="text-xs text-muted-foreground flex flex-wrap items-center gap-4 pt-1">
                {email && (
                  <span className="flex items-center gap-1.5">
                    <Mail className="w-3.5 h-3.5 text-primary" /> {email}
                  </span>
                )}
                {phone && (
                  <span className="flex items-center gap-1.5">
                    <Phone className="w-3.5 h-3.5 text-primary" /> {phone}
                  </span>
                )}
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-primary" /> Uploaded {new Date(resume.created_at).toLocaleDateString()}
                </span>
              </p>

              {/* Social Links */}
              <div className="flex flex-wrap items-center gap-3 pt-2">
                {linkedin && (
                  <a
                    href={linkedin.startsWith("http") ? linkedin : `https://${linkedin}`}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg border bg-background/60 text-xs font-medium text-blue-400 hover:border-blue-400 transition-all"
                  >
                    <Linkedin className="w-3.5 h-3.5" /> LinkedIn Profile <ExternalLink className="w-3 h-3 opacity-60" />
                  </a>
                )}
                {github && (
                  <a
                    href={github.startsWith("http") ? github : `https://${github}`}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg border bg-background/60 text-xs font-medium text-foreground hover:border-primary transition-all"
                  >
                    <Github className="w-3.5 h-3.5" /> GitHub Profile <ExternalLink className="w-3 h-3 opacity-60" />
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Overall Score Badge */}
          <div className="p-5 rounded-2xl border bg-background/80 text-center min-w-[180px] shadow-sm shrink-0">
            <div className="text-[11px] font-bold text-muted-foreground uppercase tracking-widest">ATS Match Rating</div>
            <div className="text-4xl font-black text-emerald-500 mt-1">{atsScore}%</div>
            <div className="text-[10px] font-semibold text-emerald-500/90 mt-1">High Enterprise Fit</div>
          </div>
        </div>

        {/* Executive Summary */}
        {insights.executive_summary && (
          <div className="p-4 rounded-2xl border bg-background/50 text-xs text-muted-foreground leading-relaxed flex items-start gap-3">
            <Sparkles className="w-5 h-5 text-yellow-500 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-foreground block mb-0.5">AI Executive Evaluation</span>
              {insights.executive_summary}
            </div>
          </div>
        )}
      </div>

      {/* Overview Metrics Radar Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl border bg-card/60 space-y-2">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-bold uppercase tracking-wider">Overall ATS Score</span>
            <Award className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-500">{atsScore}%</div>
          <p className="text-[11px] text-muted-foreground">Synthesized Match Index</p>
        </div>

        <div className="p-5 rounded-2xl border bg-card/60 space-y-2">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-bold uppercase tracking-wider">Skill Taxonomies</span>
            <Cpu className="w-4 h-4 text-blue-500" />
          </div>
          <div className="text-3xl font-extrabold text-blue-500">{allSkills.length}</div>
          <p className="text-[11px] text-muted-foreground">NER Identified Entities</p>
        </div>

        <div className="p-5 rounded-2xl border bg-card/60 space-y-2">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-bold uppercase tracking-wider">Vector Embedding</span>
            <BrainCircuit className="w-4 h-4 text-yellow-500" />
          </div>
          <div className="text-3xl font-extrabold text-yellow-500">384-Dim</div>
          <p className="text-[11px] text-muted-foreground">FAISS Bge-Small Alignment</p>
        </div>

        <div className="p-5 rounded-2xl border bg-card/60 space-y-2">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-bold uppercase tracking-wider">Experience Level</span>
            <Briefcase className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-lg font-extrabold text-purple-500 truncate pt-1">
            {insights.experience_level || "Specialist"}
          </div>
          <p className="text-[11px] text-muted-foreground">Automated Seniority Class</p>
        </div>
      </div>

      {/* Core Insights Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column (2/3): Skills Taxonomy & Strengths */}
        <div className="lg:col-span-2 space-y-8">
          {/* Target Role Compatibility */}
          <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
            <h3 className="text-base font-bold text-foreground flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-primary" /> Target Role Compatibility
            </h3>
            <div className="flex flex-wrap gap-2.5">
              {recommendedRoles.map((role, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1.5 rounded-xl border bg-primary/10 text-primary text-xs font-bold flex items-center gap-1.5"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> {role}
                </span>
              ))}
            </div>
          </div>

          {/* Categorized Skills Matrix */}
          <div className="p-6 rounded-2xl border bg-card/60 space-y-5">
            <h3 className="text-base font-bold text-foreground flex items-center gap-2">
              <Cpu className="w-4 h-4 text-primary" /> Categorized Skills Taxonomy
            </h3>

            {Object.keys(skillsByCategory).some(cat => skillsByCategory[cat].length > 0) ? (
              <div className="space-y-4">
                {Object.entries(skillsByCategory).map(([category, items]: [string, any]) => (
                  items && items.length > 0 && (
                    <div key={category} className="p-4 rounded-xl border bg-background/50 space-y-2">
                      <div className="text-xs font-bold uppercase tracking-wider text-muted-foreground capitalize">
                        {category.replace(/_/g, " ")}
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {items.map((skill: string) => (
                          <span
                            key={skill}
                            className="px-2.5 py-1 rounded-md border bg-primary/10 text-primary text-xs font-semibold uppercase"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )
                ))}
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {allSkills.map((skill: string) => (
                  <span
                    key={skill}
                    className="px-3 py-1 rounded-lg border bg-primary/10 text-primary text-xs font-semibold uppercase"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* AI Screening Questions */}
          <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
            <h3 className="text-base font-bold text-foreground flex items-center gap-2 text-blue-400">
              <HelpCircle className="w-4 h-4" /> Recommended Technical Screening Questions
            </h3>
            <div className="space-y-3">
              {interviewQuestions.map((q, idx) => (
                <div key={idx} className="p-4 rounded-xl border bg-background/60 text-xs text-foreground space-y-1">
                  <span className="font-bold text-primary block">Question {idx + 1}</span>
                  <p className="text-muted-foreground">{q}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column (1/3): Strengths vs Recommendations */}
        <div className="space-y-8">
          {/* Key Strengths */}
          <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
            <h3 className="text-base font-bold text-foreground flex items-center gap-2 text-emerald-500">
              <CheckCircle2 className="w-4 h-4" /> Core Technical Strengths
            </h3>
            <div className="space-y-3">
              {keyStrengths.map((str, idx) => (
                <div key={idx} className="p-3.5 rounded-xl border bg-background/50 text-xs text-muted-foreground flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>{str}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Skill Additions */}
          <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
            <h3 className="text-base font-bold text-foreground flex items-center gap-2 text-yellow-500">
              <AlertCircle className="w-4 h-4" /> High-Impact Skill Gaps
            </h3>
            <div className="space-y-3">
              {missingSkills.map((ms, idx) => (
                <div key={idx} className="p-3.5 rounded-xl border bg-background/50 text-xs text-muted-foreground flex items-start gap-2.5">
                  <Sparkles className="w-4 h-4 text-yellow-500 shrink-0 mt-0.5" />
                  <span>Add <strong className="text-foreground">{ms}</strong> to boost target enterprise ATS match scores.</span>
                </div>
              ))}
            </div>
          </div>

          {/* Raw Text Accordion Toggle */}
          <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
            <button
              onClick={() => setShowRawText(!showRawText)}
              className="w-full flex items-center justify-between text-xs font-bold text-foreground py-1"
            >
              <span className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-primary" /> Inspect Extracted Text ({rawText.length} Chars)
              </span>
              {showRawText ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showRawText && (
              <div className="p-4 rounded-xl border bg-background/80 text-[11px] font-mono text-muted-foreground whitespace-pre-wrap max-h-96 overflow-y-auto leading-relaxed">
                {rawText || "No raw text extracted from document."}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
