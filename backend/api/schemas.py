"""
Pydantic schemas for GitHub repository + AI feedback endpoints.

No AI logic lives here — only data shapes.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class RepoAnalyzeRequest(BaseModel):
    """Incoming request body: a GitHub repository URL (or owner/repo shorthand)."""

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
    """Lightweight repo info for the repo-list screen (not full detail)."""

    repo_name: str
    full_name: str
    description: Optional[str] = None
    url: str
    primary_language: Optional[str] = None
    stars: int = 0
    forks: int = 0
    updated_at: Optional[str] = None


class RepoResponse(BaseModel):
    """Structured repository information returned to the frontend."""

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
    """Incoming request body for AI repository feedback."""

    repo_url: str = Field(
        ...,
        description="GitHub repository URL to analyze",
        examples=["https://github.com/owner/repo"],
    )

    @field_validator("repo_url")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("repo_url must not be empty")
        return v.strip()


class FeedbackResponse(BaseModel):
    """AI-generated proactive feedback on a repository."""

    repo_purpose: str
    code_quality_estimate: str
    documentation_quality: str
    suggested_improvements: list[str] = Field(default_factory=list)
    missing_evidence_notes: list[str] = Field(default_factory=list)
    raw_stats: RepoResponse


class ErrorResponse(BaseModel):
    """Consistent error shape returned to the frontend."""

    error: str
    detail: Optional[str] = None