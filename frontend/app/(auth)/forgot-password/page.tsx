"use client";

import { useState } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Mail, BrainCircuit, Loader2, ArrowLeft, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";

const schema = z.object({
  email: z.string().email("Please enter a valid email"),
});

type FormData = z.infer<typeof schema>;

export default function ForgotPasswordPage() {
  const { forgotPassword, isSendingReset } = useAuth();
  const [submitted, setSubmitted] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data: FormData) => {
    forgotPassword({ email: data.email });
    setSubmitted(true);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-md"
    >
      <div className="mb-8 text-center">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-brand mb-4 shadow-lg shadow-primary/30">
          <BrainCircuit className="w-7 h-7 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-foreground">Forgot password?</h1>
        <p className="text-sm text-muted-foreground mt-1">
          We&apos;ll send you a reset link
        </p>
      </div>

      <div className="relative rounded-2xl border bg-card/60 backdrop-blur-sm p-8 shadow-xl shadow-black/20">
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/10 via-transparent to-purple-500/10 pointer-events-none" />

        {submitted ? (
          <div className="relative text-center space-y-4">
            <div className="flex justify-center">
              <CheckCircle className="w-16 h-16 text-emerald-500" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">Check your inbox</h3>
            <p className="text-sm text-muted-foreground">
              If that email is registered, we&apos;ve sent a password reset link. It expires in 1 hour.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit(onSubmit)} className="relative space-y-5">
            <div className="space-y-1.5">
              <label htmlFor="fp-email" className="text-sm font-medium text-foreground">
                Email address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  id="fp-email"
                  type="email"
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

            <button
              id="forgot-password-submit"
              type="submit"
              disabled={isSendingReset}
              className="w-full py-2.5 px-4 rounded-lg bg-gradient-brand text-white font-semibold
                text-sm shadow-lg shadow-primary/30 hover:opacity-90 active:scale-[0.98]
                transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed
                flex items-center justify-center gap-2"
            >
              {isSendingReset ? (
                <><Loader2 className="w-4 h-4 animate-spin" />Sending…</>
              ) : "Send reset link"}
            </button>
          </form>
        )}
      </div>

      <div className="text-center mt-6">
        <Link
          href="/login"
          className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to sign in
        </Link>
      </div>
    </motion.div>
  );
}
