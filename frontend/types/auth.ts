/**
 * TypeScript types for authentication.
 * Mirrors the Pydantic schemas from the backend.
 */

export type UserRole = "admin" | "recruiter" | "candidate";

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  is_email_verified: boolean;
  avatar_url: string | null;
  bio: string | null;
  created_at: string;
  last_login_at: string | null;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
  expires_in: number;
  user: User;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface MessageResponse {
  message: string;
  success: boolean;
}

export interface UpdateProfileRequest {
  name?: string;
  bio?: string;
  avatar_url?: string;
}
