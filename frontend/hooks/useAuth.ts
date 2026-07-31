/**
 * useAuth — React hook for authentication actions.
 * Coordinates the auth service, Zustand store, and TanStack Query.
 */

"use client";

import { useCallback } from "react";
import { useRouter } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { authService } from "@/services/authService";
import { useAuthStore } from "@/stores/authStore";
import type { LoginRequest, RegisterRequest, UpdateProfileRequest } from "@/types/auth";
import { tokenStorage } from "@/lib/api";

export function useAuth() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, isAuthenticated, isLoading, setUser, clearAuth } = useAuthStore();

  // ── Fetch current user (on mount if token exists) ─────────────────────────
  const { data: currentUser } = useQuery({
    queryKey: ["auth", "me"],
    queryFn: authService.getMe,
    enabled: !!tokenStorage.getToken(),
    retry: false,
    staleTime: 5 * 60 * 1000,
  });

  // ── Register ──────────────────────────────────────────────────────────────
  const registerMutation = useMutation({
    mutationFn: authService.register,
    onSuccess: (_, variables) => {
      toast.success("Account created!", {
        description: `Check ${variables.email} for your verification link.`,
      });
      router.push("/login?registered=true");
    },
    onError: (error: any) => {
      const msg = error?.response?.data?.detail ?? "Registration failed. Please try again.";
      toast.error(msg);
    },
  });

  // ── Login ─────────────────────────────────────────────────────────────────
  const loginMutation = useMutation({
    mutationFn: authService.login,
    onSuccess: (data) => {
      setUser(data.user);
      queryClient.setQueryData(["auth", "me"], data.user);
      toast.success(`Welcome back, ${data.user.name.split(" ")[0]}! 👋`);
      // Route based on role
      const dashboardRoutes: Record<string, string> = {
        admin: "/dashboard/admin",
        recruiter: "/dashboard/recruiter",
        candidate: "/dashboard/candidate",
      };
      router.push(dashboardRoutes[data.user.role] ?? "/dashboard");
    },
    onError: (error: any) => {
      const msg = error?.response?.data?.detail ?? "Invalid email or password.";
      toast.error(msg);
    },
  });

  // ── Logout ────────────────────────────────────────────────────────────────
  const logout = useCallback(() => {
    authService.logout();
    clearAuth();
    queryClient.clear();
    toast.info("You have been signed out.");
    router.push("/login");
  }, [clearAuth, queryClient, router]);

  // ── Forgot password ───────────────────────────────────────────────────────
  const forgotPasswordMutation = useMutation({
    mutationFn: ({ email }: { email: string }) =>
      authService.forgotPassword(email),
    onSuccess: () => {
      toast.success("Reset link sent!", {
        description: "Check your email for the password reset link.",
      });
    },
    onError: () => toast.error("Something went wrong. Please try again."),
  });

  // ── Update profile ────────────────────────────────────────────────────────
  const updateProfileMutation = useMutation({
    mutationFn: (data: UpdateProfileRequest) => authService.updateProfile(data),
    onSuccess: (updatedUser) => {
      setUser(updatedUser);
      queryClient.setQueryData(["auth", "me"], updatedUser);
      toast.success("Profile updated successfully.");
    },
    onError: () => toast.error("Failed to update profile."),
  });

  return {
    // State
    user: currentUser ?? user,
    isAuthenticated: isAuthenticated || !!currentUser,
    isLoading,

    // Actions
    register: registerMutation.mutate,
    login: loginMutation.mutate,
    logout,
    forgotPassword: forgotPasswordMutation.mutate,
    updateProfile: updateProfileMutation.mutate,

    // Mutation states
    isRegistering: registerMutation.isPending,
    isLoggingIn: loginMutation.isPending,
    isSendingReset: forgotPasswordMutation.isPending,
    isUpdatingProfile: updateProfileMutation.isPending,
  };
}
