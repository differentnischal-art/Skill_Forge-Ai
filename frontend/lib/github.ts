/**
 * Wrappers around the GitHub/analysis endpoints. Types here mirror
 * backend/api/schemas.py exactly, field for field.
 */

import { apiGet, apiPost } from "./api";

export interface RepoSummary {
  repo_name: string;
  full_name: string;
  description: string | null;
  url: string;
  primary_language: string | null;
  stars: number;
  forks: number;
  updated_at: string | null;
}

export interface RepoResponse {
  repo_name: string;
  full_name: string;
  owner: string;
  description: string | null;
  url: string;
  homepage: string | null;
  primary_language: string | null;
  languages: Record<string, number>;
  topics: string[];
  stars: number;
  forks: number;
  watchers: number;
  open_issues: number;
  license: string | null;
  default_branch: string;
  size_kb: number;
  is_fork: boolean;
  is_archived: boolean;
  visibility: string;
  created_at: string | null;
  updated_at: string | null;
  pushed_at: string | null;
  has_readme: boolean;
}

export interface FeedbackResponse {
  repo_purpose: string;
  code_quality_estimate: string;
  documentation_quality: string;
  suggested_improvements: string[];
  missing_evidence_notes: string[];
  files_reviewed: string[];
  total_source_files_found: number;
  raw_stats: RepoResponse;
}

export interface CareerAnalysisResponse {
  strengths: string[];
  weaknesses: string[];
  missing_skills: string[];
  career_readiness: string;
  overall_summary: string;
  repos_analyzed: number;
}

export function listUserRepos(username: string): Promise<RepoSummary[]> {
  return apiGet<RepoSummary[]>(`/api/github/repos/${encodeURIComponent(username)}`);
}

export function getRepoFeedback(repoUrl: string): Promise<FeedbackResponse> {
  return apiPost<FeedbackResponse>("/api/github/feedback", { repo_url: repoUrl });
}

export function getCareerAnalysis(
  username: string,
  careerGoal: string
): Promise<CareerAnalysisResponse> {
  return apiPost<CareerAnalysisResponse>("/api/career-analysis", {
    username,
    career_goal: careerGoal,
  });
}