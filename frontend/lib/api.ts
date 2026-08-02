/**
 * Axios API client with JWT interceptor, token refresh, and error handling.
 */

import axios, {
  AxiosError,
  AxiosInstance,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from "axios";

const rawBaseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const BASE_URL = rawBaseUrl.endsWith("/api/v1") ? rawBaseUrl : `${rawBaseUrl.replace(/\/$/, "")}/api/v1`;

// ── Token helpers ──────────────────────────────────────────────────────────────
const TOKEN_KEY = "hiresmart_access_token";
const REFRESH_TOKEN_KEY = "hiresmart_refresh_token";

export const tokenStorage = {
  getToken: () =>
    typeof window !== "undefined" ? localStorage.getItem(TOKEN_KEY) : null,
  setToken: (token: string) =>
    typeof window !== "undefined" && localStorage.setItem(TOKEN_KEY, token),
  getRefreshToken: () =>
    typeof window !== "undefined"
      ? localStorage.getItem(REFRESH_TOKEN_KEY)
      : null,
  setRefreshToken: (token: string) =>
    typeof window !== "undefined" &&
    localStorage.setItem(REFRESH_TOKEN_KEY, token),
  clearTokens: () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
    }
  },
};

// ── Create Axios instance ────────────────────────────────────────────────────
const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30_000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// ── Request interceptor — attach Bearer token ────────────────────────────────
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = tokenStorage.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ── Response interceptor — refresh token on 401 ──────────────────────────────
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value: unknown) => void;
  reject: (reason?: unknown) => void;
}> = [];

const processQueue = (error: AxiosError | null, token: string | null = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error);
    } else {
      resolve(token);
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = tokenStorage.getRefreshToken();
      if (!refreshToken) {
        tokenStorage.clearTokens();
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        const { data } = await axios.post(`${BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        tokenStorage.setToken(data.access_token);
        api.defaults.headers.common.Authorization = `Bearer ${data.access_token}`;
        processQueue(null, data.access_token);
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError as AxiosError, null);
        tokenStorage.clearTokens();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// ── Typed response helper ─────────────────────────────────────────────────────
export async function apiCall<T>(
  promise: Promise<AxiosResponse<T>>
): Promise<T> {
  const response = await promise;
  return response.data;
}
