"use client";

import { BarChart3, TrendingUp, Users, CheckCircle, Clock } from "lucide-react";

export default function AnalyticsPage() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Hiring Analytics</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Metrics, hiring funnel efficiency, and skill distribution across all job postings.
        </p>
      </div>

      {/* Funnel Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="stat-card">
          <div className="text-xs text-muted-foreground font-semibold uppercase">Total Screened</div>
          <div className="text-3xl font-extrabold mt-2">128</div>
          <div className="text-xs text-emerald-500 mt-1">100% Automated by AI</div>
        </div>

        <div className="stat-card">
          <div className="text-xs text-muted-foreground font-semibold uppercase">Qualified (&gt;75% ATS)</div>
          <div className="text-3xl font-extrabold mt-2 text-blue-500">64</div>
          <div className="text-xs text-muted-foreground mt-1">50% Conversion Rate</div>
        </div>

        <div className="stat-card">
          <div className="text-xs text-muted-foreground font-semibold uppercase">Shortlisted</div>
          <div className="text-3xl font-extrabold mt-2 text-yellow-500">18</div>
          <div className="text-xs text-muted-foreground mt-1">Ready for Interview</div>
        </div>

        <div className="stat-card">
          <div className="text-xs text-muted-foreground font-semibold uppercase">Avg Time to Screen</div>
          <div className="text-3xl font-extrabold mt-2 text-emerald-500">1.2 sec</div>
          <div className="text-xs text-emerald-500 mt-1">98% Faster than manual</div>
        </div>
      </div>

      {/* Visual Funnel Bar */}
      <div className="p-6 rounded-2xl border bg-card/60 space-y-4">
        <h2 className="text-base font-bold text-foreground">Hiring Funnel Progression</h2>
        <div className="space-y-3">
          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span>Applied / Uploaded (128)</span>
              <span>100%</span>
            </div>
            <div className="h-3 rounded-full bg-muted overflow-hidden">
              <div className="h-full bg-primary rounded-full w-full" />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span>AI ATS Score &gt; 70% (64)</span>
              <span>50%</span>
            </div>
            <div className="h-3 rounded-full bg-muted overflow-hidden">
              <div className="h-full bg-blue-500 rounded-full w-1/2" />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span>Recruiter Shortlisted (18)</span>
              <span>14%</span>
            </div>
            <div className="h-3 rounded-full bg-muted overflow-hidden">
              <div className="h-full bg-yellow-500 rounded-full w-[14%]" />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span>Hired (4)</span>
              <span>3%</span>
            </div>
            <div className="h-3 rounded-full bg-muted overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full w-[3%]" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
