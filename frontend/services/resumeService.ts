/**
 * Resume API service — handles file upload, listing, details, and deletion.
 */

import api, { apiCall } from "@/lib/api";

export interface ResumeUploadResponse {
  id: string;
  user_id: string;
  file_name: string;
  file_url: string;
  file_size: number;
  file_type: string;
  status: string;
  created_at: string;
}

export interface ResumeDetailResponse extends ResumeUploadResponse {
  parsed_text?: string;
  parsed_data: Record<string, any>;
  ats_score?: number;
  updated_at: string;
}

export const resumeService = {
  uploadResume: async (file: File): Promise<ResumeUploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post<ResumeUploadResponse>("/resume/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  getMyResumes: () => apiCall<ResumeUploadResponse[]>(api.get("/resume/my-resumes")),

  getResumeDetails: (id: string) => apiCall<ResumeDetailResponse>(api.get(`/resume/${id}`)),

  deleteResume: (id: string) => apiCall<{ message: string; success: boolean }>(api.delete(`/resume/${id}`)),
};
