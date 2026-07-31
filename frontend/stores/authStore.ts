/**
 * Zustand auth store — global authentication state.
 * Persists user to localStorage for page refresh recovery.
 */

import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { User } from "@/types/auth";
import { tokenStorage } from "@/lib/api";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: User) => void;
  clearAuth: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user: User) =>
        set({ user, isAuthenticated: true, isLoading: false }),

      clearAuth: () => {
        tokenStorage.clearTokens();
        set({ user: null, isAuthenticated: false, isLoading: false });
      },

      setLoading: (loading: boolean) => set({ isLoading: loading }),
    }),
    {
      name: "hiresmart-auth",
      storage: createJSONStorage(() =>
        typeof window !== "undefined" ? localStorage : ({} as Storage)
      ),
      // Only persist user info — tokens stay in localStorage separately
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);
