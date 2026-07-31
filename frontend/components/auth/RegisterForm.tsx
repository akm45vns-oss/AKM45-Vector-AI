"use client";

import { useState } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  Eye, EyeOff, Mail, Lock, User, BrainCircuit,
  Loader2, Briefcase, GraduationCap,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import type { UserRole } from "@/types/auth";

const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Please enter a valid email"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain an uppercase letter")
    .regex(/[a-z]/, "Must contain a lowercase letter")
    .regex(/[0-9]/, "Must contain a number"),
  role: z.enum(["candidate", "recruiter"] as const),
});

type RegisterFormData = z.infer<typeof registerSchema>;

const roles: { value: UserRole; label: string; desc: string; icon: React.ReactNode }[] = [
  {
    value: "candidate",
    label: "Job Seeker",
    desc: "Upload resume & track applications",
    icon: <GraduationCap className="w-5 h-5" />,
  },
  {
    value: "recruiter",
    label: "Recruiter",
    desc: "Post jobs & rank candidates",
    icon: <Briefcase className="w-5 h-5" />,
  },
];

export function RegisterForm() {
  const { register: registerUser, isRegistering } = useAuth();
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: { role: "candidate" },
  });

  const selectedRole = watch("role");
  const password = watch("password") ?? "";

  const onSubmit = (data: RegisterFormData) => registerUser(data);

  // Password strength indicators
  const checks = [
    { label: "8+ characters", met: password.length >= 8 },
    { label: "Uppercase", met: /[A-Z]/.test(password) },
    { label: "Lowercase", met: /[a-z]/.test(password) },
    { label: "Number", met: /[0-9]/.test(password) },
  ];
  const strength = checks.filter((c) => c.met).length;
  const strengthColor =
    strength <= 1 ? "bg-destructive" :
    strength === 2 ? "bg-yellow-500" :
    strength === 3 ? "bg-blue-500" : "bg-emerald-500";

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
        <h1 className="text-2xl font-bold text-foreground">Create your account</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Start hiring smarter with AI
        </p>
      </div>

      <div className="relative rounded-2xl border bg-card/60 backdrop-blur-sm p-8 shadow-xl shadow-black/20">
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/10 via-transparent to-purple-500/10 pointer-events-none" />

        <form onSubmit={handleSubmit(onSubmit)} className="relative space-y-5">

          {/* Role Selector */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">I am a…</label>
            <div className="grid grid-cols-2 gap-3">
              {roles.map((role) => (
                <button
                  key={role.value}
                  type="button"
                  id={`role-${role.value}`}
                  onClick={() => setValue("role", role.value)}
                  className={`relative flex flex-col items-start gap-1 p-3.5 rounded-xl border
                    text-left transition-all duration-200 cursor-pointer
                    ${selectedRole === role.value
                      ? "border-primary bg-primary/10 shadow-sm shadow-primary/20"
                      : "border-border bg-background/40 hover:border-primary/40 hover:bg-primary/5"
                    }`}
                >
                  <span className={selectedRole === role.value ? "text-primary" : "text-muted-foreground"}>
                    {role.icon}
                  </span>
                  <span className="text-sm font-semibold text-foreground">{role.label}</span>
                  <span className="text-xs text-muted-foreground leading-tight">{role.desc}</span>
                  {selectedRole === role.value && (
                    <div className="absolute top-2 right-2 w-2 h-2 rounded-full bg-primary" />
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Full Name */}
          <div className="space-y-1.5">
            <label htmlFor="name" className="text-sm font-medium text-foreground">Full name</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                id="name"
                type="text"
                autoComplete="name"
                placeholder="Jane Smith"
                {...register("name")}
                className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background/50 text-sm
                  placeholder:text-muted-foreground/60 outline-none transition-all duration-150
                  focus:ring-2 focus:ring-primary/40 focus:border-primary
                  ${errors.name ? "border-destructive" : "border-border"}`}
              />
            </div>
            {errors.name && <p className="text-xs text-destructive">{errors.name.message}</p>}
          </div>

          {/* Email */}
          <div className="space-y-1.5">
            <label htmlFor="reg-email" className="text-sm font-medium text-foreground">Email address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                id="reg-email"
                type="email"
                autoComplete="email"
                placeholder="you@company.com"
                {...register("email")}
                className={`w-full pl-10 pr-4 py-2.5 rounded-lg border bg-background/50 text-sm
                  placeholder:text-muted-foreground/60 outline-none transition-all duration-150
                  focus:ring-2 focus:ring-primary/40 focus:border-primary
                  ${errors.email ? "border-destructive" : "border-border"}`}
              />
            </div>
            {errors.email && <p className="text-xs text-destructive">{errors.email.message}</p>}
          </div>

          {/* Password */}
          <div className="space-y-1.5">
            <label htmlFor="reg-password" className="text-sm font-medium text-foreground">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                id="reg-password"
                type={showPassword ? "text" : "password"}
                autoComplete="new-password"
                placeholder="••••••••"
                {...register("password")}
                className={`w-full pl-10 pr-10 py-2.5 rounded-lg border bg-background/50 text-sm
                  placeholder:text-muted-foreground/60 outline-none transition-all duration-150
                  focus:ring-2 focus:ring-primary/40 focus:border-primary
                  ${errors.password ? "border-destructive" : "border-border"}`}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {errors.password && <p className="text-xs text-destructive">{errors.password.message}</p>}

            {/* Strength bar */}
            {password.length > 0 && (
              <AnimatePresence>
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="space-y-2"
                >
                  <div className="flex gap-1">
                    {[1, 2, 3, 4].map((i) => (
                      <div key={i} className="flex-1 h-1 rounded-full bg-muted overflow-hidden">
                        <motion.div
                          initial={{ scaleX: 0 }}
                          animate={{ scaleX: i <= strength ? 1 : 0 }}
                          className={`h-full rounded-full origin-left ${strengthColor}`}
                        />
                      </div>
                    ))}
                  </div>
                  <div className="flex flex-wrap gap-x-3 gap-y-1">
                    {checks.map((c) => (
                      <span
                        key={c.label}
                        className={`text-xs transition-colors ${c.met ? "text-emerald-500" : "text-muted-foreground"}`}
                      >
                        {c.met ? "✓" : "○"} {c.label}
                      </span>
                    ))}
                  </div>
                </motion.div>
              </AnimatePresence>
            )}
          </div>

          {/* Submit */}
          <button
            id="register-submit"
            type="submit"
            disabled={isRegistering}
            className="w-full py-2.5 px-4 rounded-lg bg-gradient-brand text-white font-semibold
              text-sm shadow-lg shadow-primary/30 hover:opacity-90 active:scale-[0.98]
              transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed
              flex items-center justify-center gap-2"
          >
            {isRegistering ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Creating account…
              </>
            ) : (
              "Create account"
            )}
          </button>

          <p className="text-center text-xs text-muted-foreground">
            By signing up you agree to our{" "}
            <Link href="/terms" className="text-primary hover:underline">Terms</Link>{" "}
            and{" "}
            <Link href="/privacy" className="text-primary hover:underline">Privacy Policy</Link>.
          </p>
        </form>
      </div>

      <p className="text-center text-sm text-muted-foreground mt-6">
        Already have an account?{" "}
        <Link href="/login" className="text-primary font-medium hover:text-primary/80 transition-colors">
          Sign in
        </Link>
      </p>
    </motion.div>
  );
}
