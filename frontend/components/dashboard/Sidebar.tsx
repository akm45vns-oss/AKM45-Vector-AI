"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BrainCircuit,
  LayoutDashboard,
  Briefcase,
  UploadCloud,
  Users,
  BarChart3,
  Settings,
  LogOut,
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const isRecruiter = user?.role === "recruiter" || user?.role === "admin";

  const navigation = [
    {
      name: "Dashboard",
      href: isRecruiter ? "/dashboard/recruiter" : "/dashboard/candidate",
      icon: LayoutDashboard,
    },
    ...(isRecruiter
      ? [
          { name: "Post New Job", href: "/jobs/create", icon: Briefcase },
          { name: "Analytics", href: "/analytics", icon: BarChart3 },
        ]
      : [
          { name: "Upload Resume", href: "/upload", icon: UploadCloud },
        ]),
    { name: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 border-r bg-card/60 backdrop-blur-md flex flex-col justify-between h-screen sticky top-0">
      <div className="p-6 space-y-8">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-brand flex items-center justify-center shadow-md shadow-primary/30">
            <BrainCircuit className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-lg text-foreground">AKM45 Vector AI</span>
        </Link>

        {/* Navigation */}
        <nav className="space-y-1.5">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`nav-item ${isActive ? "active" : ""}`}
              >
                <Icon className="w-4 h-4" />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Logout button */}
      <div className="p-4 border-t">
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-destructive hover:bg-destructive/10 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
