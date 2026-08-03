"use client";

import Link from "next/link";
import {
  BrainCircuit,
  Zap,
  Sparkles,
  Search,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  BarChart3,
  Users,
  FileCheck,
} from "lucide-react";
import { motion } from "framer-motion";
import NeuralBg from "@/components/ui/NeuralBg";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-dark text-foreground flex flex-col justify-between selection:bg-primary selection:text-white">
      {/* Navbar */}
      <nav className="border-b border-border/40 backdrop-blur-md bg-background/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-brand flex items-center justify-center shadow-lg shadow-primary/30">
              <BrainCircuit className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight">AKM45 Vector AI</span>
          </div>

          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
            <a href="#features" className="hover:text-foreground transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-foreground transition-colors">How It Works</a>
            <a href="#pricing" className="hover:text-foreground transition-colors">Pricing</a>
          </div>

          <div className="flex items-center gap-4">
            <Link
              href="/login"
              className="text-sm font-semibold text-muted-foreground hover:text-foreground transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/register"
              className="py-2 px-4 rounded-lg bg-gradient-brand text-white text-sm font-semibold shadow-lg shadow-primary/30 hover:opacity-90 transition-all active:scale-95"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section with Neural WebGL Background */}
      <NeuralBg hue={200} saturation={0.8} chroma={0.6} className="py-24 px-6 border-b border-border/30">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6 max-w-4xl mx-auto"
          >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-primary/30 bg-primary/10 text-primary text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" /> Next-Gen AI Resume Screening Platform
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight leading-tight">
            Stop Manual Resume Screening. <br />
            <span className="gradient-text">Hire Top 1% Candidates in Seconds.</span>
          </h1>

          <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            AKM45 Vector AI parses resumes, extracts candidate skills with NER, performs semantic vector search, and delivers LLM-powered candidate evaluations instantly.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link
              href="/register"
              className="w-full sm:w-auto py-3.5 px-8 rounded-xl bg-gradient-brand text-white font-semibold text-base shadow-xl shadow-primary/30 hover:opacity-90 transition-all flex items-center justify-center gap-2"
            >
              Start Screening Free <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/login"
              className="w-full sm:w-auto py-3.5 px-8 rounded-xl border border-border bg-card/50 text-foreground font-semibold text-base hover:bg-card transition-all"
            >
              View Recruiter Demo
            </Link>
          </div>
        </motion.div>
      </div>
    </NeuralBg>

      {/* Feature Grid */}
      <section id="features" className="py-20 px-6 max-w-7xl mx-auto w-full">
        <div className="text-center mb-16 space-y-3">
          <h2 className="text-3xl font-bold">Engineered for Modern Talent Teams</h2>
          <p className="text-muted-foreground text-sm max-w-xl mx-auto">
            Everything you need to automate hiring pipelines from resume ingest to final interview decision.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-8 rounded-2xl border bg-card/40 backdrop-blur-sm space-y-4 hover:border-primary/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <Zap className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold">Automated Resume Parsing</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Extract contact info, work experience, education, and 500+ skills from PDF and DOCX files automatically.
            </p>
          </div>

          <div className="p-8 rounded-2xl border bg-card/40 backdrop-blur-sm space-y-4 hover:border-primary/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold">FAISS Semantic Search</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Query candidates using natural language instead of rigid keywords. Powered by BAEI/bge vector embeddings.
            </p>
          </div>

          <div className="p-8 rounded-2xl border bg-card/40 backdrop-blur-sm space-y-4 hover:border-primary/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <BrainCircuit className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold">Llama 3 Candidate Reports</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Receive AI generated candidate summaries, strengths, missing skills, and tailored technical interview questions.
            </p>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-6 max-w-7xl mx-auto w-full">
        <div className="text-center mb-16 space-y-3">
          <h2 className="text-3xl font-bold">Simple, Transparent Pricing</h2>
          <p className="text-muted-foreground text-sm">Scale your hiring without per-seat markup.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Free Tier */}
          <div className="p-8 rounded-2xl border bg-card/40 flex flex-col justify-between space-y-6">
            <div>
              <h3 className="text-lg font-bold">Starter</h3>
              <div className="text-3xl font-extrabold mt-2">$0 <span className="text-xs text-muted-foreground font-normal">/ month</span></div>
              <ul className="mt-6 space-y-3 text-sm text-muted-foreground">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Up to 50 Resumes/mo</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Automated ATS Scoring</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> 1 Active Job Posting</li>
              </ul>
            </div>
            <Link href="/register" className="w-full py-2.5 rounded-lg border border-border text-center text-sm font-semibold hover:bg-card">Get Started Free</Link>
          </div>

          {/* Pro Tier */}
          <div className="p-8 rounded-2xl border-2 border-primary bg-card/80 flex flex-col justify-between space-y-6 relative shadow-2xl shadow-primary/20">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white text-xs font-bold px-3 py-1 rounded-full">MOST POPULAR</div>
            <div>
              <h3 className="text-lg font-bold">Growth Pro</h3>
              <div className="text-3xl font-extrabold mt-2">$99 <span className="text-xs text-muted-foreground font-normal">/ month</span></div>
              <ul className="mt-6 space-y-3 text-sm text-muted-foreground">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Unlimited Resumes</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> FAISS Vector Semantic Search</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Llama 3 AI Candidate Reports</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> 20 Active Job Postings</li>
              </ul>
            </div>
            <Link href="/register" className="w-full py-2.5 rounded-lg bg-gradient-brand text-white text-center text-sm font-semibold shadow-lg shadow-primary/30">Start 14-Day Trial</Link>
          </div>

          {/* Enterprise */}
          <div className="p-8 rounded-2xl border bg-card/40 flex flex-col justify-between space-y-6">
            <div>
              <h3 className="text-lg font-bold">Enterprise</h3>
              <div className="text-3xl font-extrabold mt-2">Custom</div>
              <ul className="mt-6 space-y-3 text-sm text-muted-foreground">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Custom LLM Fine-Tuning</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Dedicated Storage & VPC</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> 24/7 SLA & Dedicated Rep</li>
              </ul>
            </div>
            <Link href="/register" className="w-full py-2.5 rounded-lg border border-border text-center text-sm font-semibold hover:bg-card">Contact Sales</Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/40 py-10 px-6 text-center text-xs text-muted-foreground">
        <p>© 2026 AKM45 Vector AI Inc. All rights reserved. Built with Next.js 15, FastAPI, and FAISS.</p>
      </footer>
    </div>
  );
}
