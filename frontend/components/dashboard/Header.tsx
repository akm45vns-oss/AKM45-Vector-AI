"use client";

import { useAuth } from "@/hooks/useAuth";
import { User, Bell } from "lucide-react";

export function Header() {
  const { user } = useAuth();

  return (
    <header className="h-16 border-b bg-card/40 backdrop-blur-md px-8 flex items-center justify-between sticky top-0 z-40">
      <div>
        <h2 className="text-sm font-semibold text-foreground">
          Welcome back, <span className="gradient-text">{user?.name || "User"}</span>
        </h2>
        <p className="text-xs text-muted-foreground capitalize">Role: {user?.role || "Candidate"}</p>
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors relative">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-primary" />
        </button>

        <div className="flex items-center gap-3 border-l pl-4">
          <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-xs">
            {user?.name ? user.name[0].toUpperCase() : <User className="w-4 h-4" />}
          </div>
        </div>
      </div>
    </header>
  );
}
