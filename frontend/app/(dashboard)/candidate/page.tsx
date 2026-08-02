"use client";

import { useEffect, useState } from "react";
import { UploadCloud, FileText, CheckCircle2, Sparkles, ArrowRight, Clock, Award } from "lucide-react";
import Link from "next/link";
import { resumeService, ResumeUploadResponse } from "@/services/resumeService";

export default function CandidateDashboard() {
  const [resumes, setResumes] = useState<ResumeUploadResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        setLoading(true);
        const data = await resumeService.getMyResumes();
        setResumes(data);
      } catch (err) {
        console.error("Error fetching resumes:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, []);

  const latestResume = resumes.length > 0 ? resumes[0] : null;

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Top Banner */}
      <div className="p-6 rounded-2xl bg-card border shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Candidate Dashboard</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Track your uploaded resume status, view ATS score breakdowns, and monitor job applications.
          </p>
        </div>

        <Link
          href="/upload"
          className="py-2.5 px-4 rounded-xl bg-gradient-brand text-white font-semibold text-sm shadow-md shadow-primary/30 flex items-center gap-2 hover:opacity-90 transition-all"
        >
          <UploadCloud className="w-4 h-4" /> Upload New Resume
        </Link>
      </div>

      {/* Active Resume Details */}
      {loading ? (
        <div className="p-8 rounded-2xl border bg-card/60 text-center animate-pulse">
          <div className="text-sm font-semibold text-muted-foreground">Loading candidate resumes...</div>
        </div>
      ) : latestResume ? (
        <div className="p-6 rounded-2xl border bg-card/60 backdrop-blur-sm space-y-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-base font-bold text-foreground">{latestResume.file_name}</h2>
                <p className="text-xs text-muted-foreground">
                  Uploaded on {new Date(latestResume.created_at).toLocaleDateString()} • {latestResume.file_type.toUpperCase()} Format
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 text-xs font-bold border border-emerald-500/20">
                Parsed & Indexed
              </span>
              <Link
                href={`/candidate/resume/${latestResume.id}`}
                className="py-2 px-3.5 rounded-xl bg-primary text-white text-xs font-semibold flex items-center gap-1.5 hover:opacity-90 transition-all shadow-sm"
              >
                View Parsed Details <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>

          {/* ATS Score Meter */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
            <div className="p-4 rounded-xl border bg-background/50 text-center">
              <div className="text-xs text-muted-foreground font-semibold uppercase">Overall ATS Score</div>
              <div className="text-3xl font-extrabold text-emerald-500 mt-1">88.5%</div>
              <div className="text-[10px] text-muted-foreground mt-1">Strong Match Potential</div>
            </div>

            <div className="p-4 rounded-xl border bg-background/50 text-center">
              <div className="text-xs text-muted-foreground font-semibold uppercase">Skill Match</div>
              <div className="text-3xl font-extrabold text-blue-500 mt-1">92.0%</div>
              <div className="text-[10px] text-muted-foreground mt-1">NER Entities Extracted</div>
            </div>

            <div className="p-4 rounded-xl border bg-background/50 text-center">
              <div className="text-xs text-muted-foreground font-semibold uppercase">Semantic Score</div>
              <div className="text-3xl font-extrabold text-yellow-500 mt-1">85.0%</div>
              <div className="text-[10px] text-muted-foreground mt-1">FAISS Cosine Similarity</div>
            </div>

            <div className="p-4 rounded-xl border bg-background/50 text-center">
              <div className="text-xs text-muted-foreground font-semibold uppercase">Experience Match</div>
              <div className="text-3xl font-extrabold text-purple-500 mt-1">90.0%</div>
              <div className="text-[10px] text-muted-foreground mt-1">Years Detected</div>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-8 rounded-2xl border bg-card/60 text-center space-y-4">
          <div className="w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center mx-auto">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-foreground">No Resumes Uploaded Yet</h3>
            <p className="text-xs text-muted-foreground mt-1">
              Upload your PDF or DOCX resume to analyze your ATS score and match with open jobs.
            </p>
          </div>
          <Link
            href="/upload"
            className="inline-flex items-center gap-2 py-2 px-4 rounded-xl bg-primary text-white text-xs font-semibold shadow-md"
          >
            <UploadCloud className="w-4 h-4" /> Upload Resume
          </Link>
        </div>
      )}

      {/* Extracted Skills & Suggestions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
          <h3 className="text-base font-bold text-foreground">Parsed Skills Taxonomy</h3>
          <div className="flex flex-wrap gap-2">
            {["Python", "FastAPI", "Next.js", "TypeScript", "PostgreSQL", "Docker", "AWS", "Git", "REST APIs", "Pytest"].map((skill) => (
              <span key={skill} className="px-2.5 py-1 rounded-md border bg-primary/10 text-primary text-xs font-semibold">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
          <div className="flex items-center gap-2 text-yellow-500 font-bold text-base">
            <Sparkles className="w-5 h-5" /> AI Recommendations
          </div>
          <ul className="space-y-2 text-xs text-muted-foreground">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
              <span>Add explicit mentions of Kubernetes or Terraform to increase DevOps match scores.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
              <span>Quantify project achievements with metrics (e.g. &quot;Reduced latency by 40%&quot;).</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
