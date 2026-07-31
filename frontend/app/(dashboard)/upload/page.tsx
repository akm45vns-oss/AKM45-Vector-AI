"use client";

import { useState } from "react";
import { ResumeUploader } from "@/components/resume/ResumeUploader";
import { ResumeUploadResponse } from "@/services/resumeService";
import { FileText, Sparkles, CheckCircle2, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function UploadResumePage() {
  const [uploadedResume, setUploadedResume] = useState<ResumeUploadResponse | null>(null);

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Upload Resume</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Upload your resume in PDF or DOCX format. Our AI will automatically parse your skills, experience, and calculate your ATS match score.
        </p>
      </div>

      {/* Upload Box */}
      <div className="bg-card border rounded-2xl p-6 shadow-sm">
        <ResumeUploader onSuccess={(resume) => setUploadedResume(resume)} />
      </div>

      {/* Uploaded Confirmation / Next Steps */}
      {uploadedResume && (
        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-2xl p-6 space-y-4">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="w-6 h-6 text-emerald-500 shrink-0" />
            <div>
              <h3 className="text-base font-semibold text-foreground">Resume Ready for Processing</h3>
              <p className="text-sm text-muted-foreground">
                File <span className="font-mono text-foreground">{uploadedResume.file_name}</span> has been saved.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4 pt-2">
            <Link
              href={`/candidate/resume/${uploadedResume.id}`}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-primary/90 transition-colors"
            >
              <Sparkles className="w-4 h-4" /> View AI Parsed Results <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
        <div className="p-4 rounded-xl border bg-card/40 space-y-1">
          <div className="text-primary font-bold text-sm">PDF or DOCX</div>
          <p className="text-xs text-muted-foreground">Clean, standard layout resumes yield the highest accuracy parsing scores.</p>
        </div>
        <div className="p-4 rounded-xl border bg-card/40 space-y-1">
          <div className="text-primary font-bold text-sm">Automatic NER</div>
          <p className="text-xs text-muted-foreground">Extracts candidate contact details, skills, education, and years of experience.</p>
        </div>
        <div className="p-4 rounded-xl border bg-card/40 space-y-1">
          <div className="text-primary font-bold text-sm">Semantic Matching</div>
          <p className="text-xs text-muted-foreground">Converts resume into vector embeddings for instant Job Matching.</p>
        </div>
      </div>
    </div>
  );
}
