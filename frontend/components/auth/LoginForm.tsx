"use client";

import { useState } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Eye, EyeOff, Mail, Lock, Loader2, BrainCircuit } from "lucide-react";
import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";

const loginSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string().min(1, "Password is required"),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { login, isLoggingIn } = useAuth();
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data: LoginFormData) => login(data);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="w-full max-w-md"
    >
      {/* Logo */}
      <div className="mb-8 text-center">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-brand mb-4 shadow-lg shadow-primary/30">
          <BrainCircuit className="w-7 h-7 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-foreground">Welcome back</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Sign in to your AKM45 Vector AI account
        </p>
      </div>

      {/* Card */}
      <div className="relative rounded-2xl border bg-card/60 backdrop-blur-sm p-8 shadow-xl shadow-black/20">
        {/* Subtle gradient border effect */}
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/10 via-transparent to-purple-500/10 pointer-events-none" />

        <form onSubmit={handleSubmit(onSubmit)} className="relative space-y-5">
          {/* Email */}
          <div className="space-y-1.5">
            <label htmlFor="email" className="text-sm font-medium text-foreground">
              Email address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                id="email"
                type="email"
                autoComplete="email"
                placeholder="you@company.com"
                {...register("email")}
                className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background/50 text-sm
                  placeholder:text-muted-foreground/60 outline-none transition-all duration-150
                  focus:ring-2 focus:ring-primary/40 focus:border-primary
                  ${errors.email ? "border-destructive focus:ring-destructive/30" : "border-border"}`}
              />
            </div>
            {errors.email && (
              <p className="text-xs text-destructive">{errors.email.message}</p>
            )}
          </div>

          {/* Password */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label htmlFor="password" className="text-sm font-medium text-foreground">
                Password
              </label>
              <Link
                href="/forgot-password"
                className="text-xs text-primary hover:text-primary/80 transition-colors"
              >
                Forgot password?
              </Link>
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                placeholder="••••••••"
                {...register("password")}
                className={`w-full pl-10 pr-10 py-2.5 rounded-lg border bg-background/50 text-sm
                  placeholder:text-muted-foreground/60 outline-none transition-all duration-150
                  focus:ring-2 focus:ring-primary/40 focus:border-primary
                  ${errors.password ? "border-destructive focus:ring-destructive/30" : "border-border"}`}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {errors.password && (
              <p className="text-xs text-destructive">{errors.password.message}</p>
            )}
          </div>

          {/* Submit */}
          <button
            id="login-submit"
            type="submit"
            disabled={isLoggingIn}
            className="w-full py-2.5 px-4 rounded-lg bg-gradient-brand text-white font-semibold
              text-sm shadow-lg shadow-primary/30 hover:opacity-90 active:scale-[0.98]
              transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed
              flex items-center justify-center gap-2"
          >
            {isLoggingIn ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Signing in…
              </>
            ) : (
              "Sign in"
            )}
          </button>
        </form>
      </div>

      {/* Footer */}
      <p className="text-center text-sm text-muted-foreground mt-6">
        Don&apos;t have an account?{" "}
        <Link
          href="/register"
          className="text-primary font-medium hover:text-primary/80 transition-colors"
        >
          Create one free
        </Link>
      </p>
    </motion.div>
  );
}
