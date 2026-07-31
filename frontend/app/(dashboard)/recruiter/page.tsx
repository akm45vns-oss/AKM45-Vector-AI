"use client";

import { Briefcase, Users, FileCheck, Sparkles, Plus, ArrowUpRight, Search } from "lucide-react";
import Link from "next/link";

export default function RecruiterDashboard() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-2xl bg-card border shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Recruiter Dashboard</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Manage your open jobs, screen incoming candidates, and review AI rankings.
          </p>
        </div>

        <Link
          href="/jobs/create"
          className="py-2.5 px-4 rounded-xl bg-gradient-brand text-white font-semibold text-sm shadow-md shadow-primary/30 flex items-center gap-2 hover:opacity-90 transition-all"
        >
          <Plus className="w-4 h-4" /> Create New Job
        </Link>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="stat-card">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Active Jobs</span>
            <Briefcase className="w-5 h-5 text-primary" />
          </div>
          <div className="text-3xl font-extrabold text-foreground mt-3">4</div>
          <p className="text-xs text-emerald-500 mt-2 flex items-center gap-1">
            <ArrowUpRight className="w-3.5 h-3.5" /> +2 this week
          </p>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Applications</span>
            <Users className="w-5 h-5 text-blue-500" />
          </div>
          <div className="text-3xl font-extrabold text-foreground mt-3">128</div>
          <p className="text-xs text-emerald-500 mt-2 flex items-center gap-1">
            <ArrowUpRight className="w-3.5 h-3.5" /> +14 today
          </p>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Avg ATS Match</span>
            <Sparkles className="w-5 h-5 text-yellow-500" />
          </div>
          <div className="text-3xl font-extrabold text-foreground mt-3">78.4%</div>
          <p className="text-xs text-muted-foreground mt-2">High accuracy semantic score</p>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Shortlisted</span>
            <FileCheck className="w-5 h-5 text-emerald-500" />
          </div>
          <div className="text-3xl font-extrabold text-foreground mt-3">18</div>
          <p className="text-xs text-muted-foreground mt-2">Ready for interview</p>
        </div>
      </div>

      {/* Active Jobs & Candidate Search */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Active Jobs List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-foreground">Active Job Postings</h2>
            <Link href="/jobs" className="text-xs text-primary font-medium hover:underline">View All</Link>
          </div>

          <div className="space-y-3">
            {[
              { id: "1", title: "Senior Python Developer", location: "Remote", applicants: 42, topScore: 94.2 },
              { id: "2", title: "Full Stack Next.js Engineer", location: "San Francisco, CA", applicants: 31, topScore: 91.0 },
              { id: "3", title: "AI / ML Architect", location: "Remote", applicants: 19, topScore: 88.5 },
              { id: "4", title: "DevOps Engineer (AWS/K8s)", location: "New York, NY", applicants: 36, topScore: 86.0 },
            ].map((job) => (
              <div key={job.id} className="p-5 rounded-xl border bg-card/60 backdrop-blur-sm flex items-center justify-between hover:border-primary/40 transition-colors">
                <div>
                  <h3 className="font-semibold text-base text-foreground">{job.title}</h3>
                  <div className="flex items-center gap-3 text-xs text-muted-foreground mt-1">
                    <span>{job.location}</span>
                    <span>•</span>
                    <span>{job.applicants} Applicants</span>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right hidden sm:block">
                    <div className="text-xs text-muted-foreground">Top Candidate</div>
                    <div className="text-sm font-bold text-emerald-500">{job.topScore}% ATS</div>
                  </div>

                  <Link
                    href={`/jobs/${job.id}/rankings`}
                    className="py-2 px-3.5 rounded-lg border border-border bg-background text-xs font-semibold hover:bg-card transition-colors"
                  >
                    View Rankings
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Semantic Search Widget */}
        <div className="space-y-4">
          <h2 className="text-lg font-bold text-foreground">Semantic Search</h2>
          <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
            <p className="text-xs text-muted-foreground">
              Search candidates semantically across your talent database using natural language queries.
            </p>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="e.g. FastAPI & PyTorch developer with Docker..."
                className="w-full pl-9 pr-3 py-2 rounded-lg border bg-background/50 text-xs outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <button className="w-full py-2 rounded-lg bg-primary text-white text-xs font-semibold shadow-md shadow-primary/20 hover:bg-primary/90">
              Run FAISS Vector Search
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
