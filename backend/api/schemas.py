"""
Pydantic schemas for GitHub repository, AI feedback, career analysis,
and authentication endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class RepoAnalyzeRequest(BaseModel):
    repo_url: str = Field(
        ...,
        description="GitHub repository URL, e.g. https://github.com/owner/repo",
        examples=["https://github.com/vercel/next.js"],
    )

    @field_validator("repo_url")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("repo_url must not be empty")
        return v.strip()


class RepoSummary(BaseModel):
    repo_name: str
    full_name: str
    description: Optional[str] = None
    url: str
    primary_language: Optional[str] = None
    stars: int = 0
    forks: int = 0
    updated_at: Optional[str] = None


class RepoResponse(BaseModel):
    repo_name: str
    full_name: str
    owner: str
    description: Optional[str] = None
    url: str
    homepage: Optional[str] = None
    primary_language: Optional[str] = None
    languages: dict[str, int] = Field(default_factory=dict)
    topics: list[str] = Field(default_factory=list)
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    open_issues: int = 0
    license: Optional[str] = None
    default_branch: str = "main"
    size_kb: int = 0
    is_fork: bool = False
    is_archived: bool = False
    visibility: str = "public"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    pushed_at: Optional[str] = None
    has_readme: bool = False


class FeedbackRequest(BaseModel):
    repo_url: str = Field(..., description="GitHub repository URL to analyze")

    @field_validator("repo_url")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("repo_url must not be empty")
        return v.strip()


class FeedbackResponse(BaseModel):
    repo_purpose: str
    code_quality_estimate: str
    documentation_quality: str
    suggested_improvements: list[str] = Field(default_factory=list)
    missing_evidence_notes: list[str] = Field(default_factory=list)
    files_reviewed: list[str] = Field(default_factory=list)
    total_source_files_found: int = 0
    raw_stats: RepoResponse


class CareerAnalysisRequest(BaseModel):
    username: str = Field(..., description="GitHub username to analyze")
    career_goal: str = Field(..., description="e.g. 'Backend Engineer', 'ML Engineer'")

    @field_validator("username", "career_goal")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be empty")
        return v.strip()


class CareerAnalysisResponse(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    career_readiness: str
    overall_summary: str
    repos_analyzed: int


class UserResponse(BaseModel):
    """Returned by /api/auth/me and after login."""

    id: int
    github_id: int
    username: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    career_goal: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None