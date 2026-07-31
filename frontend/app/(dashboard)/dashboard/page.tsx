/**
 * Minimal dashboard placeholder — replaced in Phase 9.
 * Redirects based on role; shows loading state meanwhile.
 */
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Loader2, BrainCircuit } from "lucide-react";

export default function DashboardPage() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    if (user) {
      const routes: Record<string, string> = {
        admin: "/dashboard/admin",
        recruiter: "/dashboard/recruiter",
        candidate: "/dashboard/candidate",
      };
      router.push(routes[user.role] ?? "/dashboard/candidate");
    }
  }, [user, isAuthenticated, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-dark">
      <div className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-brand shadow-xl shadow-primary/30">
          <BrainCircuit className="w-8 h-8 text-white" />
        </div>
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span>Loading your dashboard…</span>
        </div>
      </div>
    </div>
  );
}
