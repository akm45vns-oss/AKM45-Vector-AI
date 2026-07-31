/**
 * Auth API service — wraps all /auth/* endpoints.
 */

import api, { apiCall, tokenStorage } from "@/lib/api";
import type {
  LoginRequest,
  MessageResponse,
  RegisterRequest,
  TokenResponse,
  UpdateProfileRequest,
  User,
} from "@/types/auth";

export const authService = {
  register: (data: RegisterRequest) =>
    apiCall<MessageResponse>(api.post("/auth/register", data)),

  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await apiCall<TokenResponse>(api.post("/auth/login", data));
    tokenStorage.setToken(response.access_token);
    tokenStorage.setRefreshToken(response.refresh_token);
    return response;
  },

  logout: () => {
    tokenStorage.clearTokens();
  },

  getMe: () => apiCall<User>(api.get("/auth/me")),

  updateProfile: (data: UpdateProfileRequest) =>
    apiCall<User>(api.patch("/auth/me", data)),

  verifyEmail: (token: string) =>
    apiCall<MessageResponse>(api.post("/auth/verify-email", { token })),

  resendVerification: (email: string) =>
    apiCall<MessageResponse>(
      api.post("/auth/resend-verification", { email })
    ),

  forgotPassword: (email: string) =>
    apiCall<MessageResponse>(
      api.post("/auth/forgot-password", { email })
    ),

  resetPassword: (token: string, new_password: string) =>
    apiCall<MessageResponse>(
      api.post("/auth/reset-password", { token, new_password })
    ),

  refreshTokens: (refresh_token: string) =>
    apiCall<TokenResponse>(
      api.post("/auth/refresh", { refresh_token })
    ),
};
