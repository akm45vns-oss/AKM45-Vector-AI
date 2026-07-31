/**
 * Auth layout — shared animated background for login/register pages.
 */

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sign In — AKM45 Vector AI",
};

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex bg-gradient-dark relative overflow-hidden">
      {/* Animated background orbs */}
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute -top-48 -left-48 w-96 h-96 rounded-full opacity-20 blur-3xl animate-pulse-scale"
          style={{ background: "hsl(224, 80%, 55%)" }}
        />
        <div
          className="absolute -bottom-48 -right-48 w-96 h-96 rounded-full opacity-15 blur-3xl animate-pulse-scale"
          style={{ background: "hsl(262, 80%, 60%)", animationDelay: "1s" }}
        />
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full opacity-5 blur-3xl"
          style={{ background: "hsl(224, 80%, 55%)" }}
        />
      </div>

      {/* Left panel — branding (hidden on mobile) */}
      <div className="hidden lg:flex flex-col justify-between w-[480px] p-12 relative z-10">
        <div>
          <div className="flex items-center gap-3 mb-16">
            <div className="w-10 h-10 rounded-xl bg-gradient-brand flex items-center justify-center shadow-lg shadow-primary/30">
              <span className="text-white font-bold text-lg">A</span>
            </div>
            <span className="text-xl font-bold text-foreground">AKM45 Vector AI</span>
          </div>

          <div className="space-y-6">
            <h2 className="text-4xl font-bold text-foreground leading-tight">
              Hire smarter
              <br />
              <span className="gradient-text">with AI</span>
            </h2>
            <p className="text-muted-foreground text-lg leading-relaxed">
              The intelligent ATS that reads, ranks, and explains every resume.
              Stop guessing. Start hiring.
            </p>
          </div>

          {/* Feature bullets */}
          <div className="mt-12 space-y-4">
            {[
              { icon: "🧠", text: "AI parses resumes in seconds" },
              { icon: "⚡", text: "Rank 100s of candidates instantly" },
              { icon: "💡", text: "LLM explains every score" },
              { icon: "🔍", text: "Semantic search across all applicants" },
            ].map((f) => (
              <div key={f.text} className="flex items-center gap-3">
                <span className="text-xl">{f.icon}</span>
                <span className="text-sm text-muted-foreground">{f.text}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Testimonial */}
        <blockquote className="border-l-2 border-primary/40 pl-4">
          <p className="text-sm text-muted-foreground italic">
            &ldquo;HireSmart AI cut our screening time by 80%. We hired our best
            engineer in 3 days.&rdquo;
          </p>
          <footer className="text-xs text-muted-foreground/60 mt-2">
            — CTO at a Series B startup
          </footer>
        </blockquote>
      </div>

      {/* Right panel — form */}
      <div className="flex flex-1 items-center justify-center p-6 relative z-10">
        {children}
      </div>
    </div>
  );
}
