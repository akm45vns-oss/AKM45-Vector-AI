"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { resumeService, ResumeUploadResponse } from "@/services/resumeService";

interface ResumeUploaderProps {
  onSuccess?: (resume: ResumeUploadResponse) => void;
}

export function ResumeUploader({ onSuccess }: ResumeUploaderProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const selected = acceptedFiles[0];
      setFile(selected);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setUploadProgress(20);

    try {
      setUploadProgress(60);
      const result = await resumeService.uploadResume(file);
      setUploadProgress(100);
      toast.success("Resume uploaded successfully!", {
        description: `${file.name} is ready for AI parsing.`,
      });
      setFile(null);
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error: any) {
      const msg = error?.response?.data?.detail || "Failed to upload resume.";
      toast.error(msg);
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const removeFile = () => setFile(null);

  return (
    <div className="w-full max-w-2xl mx-auto space-y-4">
      {/* Dropzone Container */}
      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200
          ${isDragActive
            ? "border-primary bg-primary/10 scale-[1.01]"
            : "border-border bg-card/40 hover:border-primary/50 hover:bg-card/80"
          }
          ${file ? "border-emerald-500/50 bg-emerald-500/5" : ""}
        `}
      >
        <input {...getInputProps()} />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary shadow-inner">
            <UploadCloud className="w-7 h-7" />
          </div>

          <div>
            <h3 className="text-base font-semibold text-foreground">
              {isDragActive ? "Drop your resume here" : "Upload your resume"}
            </h3>
            <p className="text-sm text-muted-foreground mt-1">
              Drag and drop your document here, or click to browse
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs text-muted-foreground/70 bg-muted/50 px-3 py-1.5 rounded-full">
            <span>Supports PDF or DOCX</span>
            <span>•</span>
            <span>Max 10MB</span>
          </div>
        </div>
      </div>

      {/* Validation Errors */}
      {fileRejections.length > 0 && (
        <div className="flex items-center gap-2 p-3 rounded-lg border border-destructive/30 bg-destructive/10 text-xs text-destructive">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>Please select a valid PDF or DOCX file under 10MB.</span>
        </div>
      )}

      {/* Selected File Preview Card */}
      <AnimatePresence>
        {file && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex items-center justify-between p-4 rounded-xl border bg-card/80 backdrop-blur-sm shadow-sm"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground truncate max-w-xs">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {!uploading && (
                <button
                  type="button"
                  onClick={removeFile}
                  className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              )}

              <button
                type="button"
                onClick={handleUpload}
                disabled={uploading}
                className="py-2 px-4 rounded-lg bg-gradient-brand text-white text-sm font-semibold
                  shadow-md shadow-primary/20 hover:opacity-90 active:scale-95 transition-all
                  disabled:opacity-50 flex items-center gap-2"
              >
                {uploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="w-4 h-4" />
                    Upload File
                  </>
                )}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Upload Progress Bar */}
      {uploading && (
        <div className="w-full bg-muted h-2 rounded-full overflow-hidden">
          <motion.div
            className="bg-gradient-brand h-full rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${uploadProgress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      )}
    </div>
  );
}
