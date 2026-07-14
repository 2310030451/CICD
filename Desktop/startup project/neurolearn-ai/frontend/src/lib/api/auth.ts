import { apiClient } from "./client";
import { User } from "@/types";

export interface LoginRequest {
  firebase_token: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  display_name: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export const authApi = {
  async verifyToken(firebaseToken: string): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>("/api/v1/auth/firebase", {
      firebase_token: firebaseToken,
    });
  },

  async register(data: RegisterRequest): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>("/api/v1/auth/register", data);
  },

  async login(data: LoginRequest): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>("/api/v1/auth/login", data);
  },

  async logout(): Promise<void> {
    return apiClient.post("/api/v1/auth/logout");
  },

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>("/api/v1/auth/refresh", {
      refresh_token: refreshToken,
    });
  },

  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>("/api/v1/auth/me");
  },
};
