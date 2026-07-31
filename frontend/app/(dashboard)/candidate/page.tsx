"use client";

import { UploadCloud, FileText, CheckCircle2, AlertTriangle, Sparkles, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function CandidateDashboard() {
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

      {/* Resume ATS Score Card */}
      <div className="p-6 rounded-2xl border bg-card/60 backdrop-blur-sm space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-foreground">Active Resume Document</h2>
              <p className="text-xs text-muted-foreground">Uploaded 2 days ago • PDF Format</p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 text-xs font-bold">
            Parsed & Indexed
          </span>
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
            <div className="text-[10px] text-muted-foreground mt-1">12 Skills Identified</div>
          </div>

          <div className="p-4 rounded-xl border bg-background/50 text-center">
            <div className="text-xs text-muted-foreground font-semibold uppercase">Semantic Score</div>
            <div className="text-3xl font-extrabold text-yellow-500 mt-1">85.0%</div>
            <div className="text-[10px] text-muted-foreground mt-1">FAISS Cosine Similarity</div>
          </div>

          <div className="p-4 rounded-xl border bg-background/50 text-center">
            <div className="text-xs text-muted-foreground font-semibold uppercase">Experience Match</div>
            <div className="text-3xl font-extrabold text-purple-500 mt-1">90.0%</div>
            <div className="text-[10px] text-muted-foreground mt-1">5+ Years Detected</div>
          </div>
        </div>
      </div>

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
