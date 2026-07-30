/**
 * Session helpers. The JWT is stored in localStorage after the OAuth
 * callback and attached as a Bearer token on subsequent API calls.
 */

import { apiGet, API_BASE_URL } from "./api";

const TOKEN_KEY = "skillforge_token";

export function saveToken(token: string) {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(TOKEN_KEY, token);
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(TOKEN_KEY);
  }
}

export function githubLoginUrl(): string {
  return `${API_BASE_URL}/api/auth/github/login`;
}

export interface CurrentUser {
  id: number;
  github_id: number;
  username: string;
  avatar_url: string | null;
  bio: string | null;
  career_goal: string | null;
}

export function fetchCurrentUser(token: string): Promise<CurrentUser> {
  return apiGet<CurrentUser>("/api/auth/me", token);
}