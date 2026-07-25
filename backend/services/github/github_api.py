"""
GitHub data-fetching service.

Talks to the GitHub REST API only. Contains zero AI / prompting logic —
per system_design.md this layer's only job is to normalize GitHub data
into a clean shape. Feature extraction / prompt-building comes later.
"""

import os
from typing import Optional

import httpx

from models.schemas import RepoResponse
from utils.helpers import parse_github_url

GITHUB_API_BASE = "https://api.github.com"


class GitHubServiceError(Exception):
    """Raised for any GitHub-fetch failure, carrying an HTTP-friendly status code."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _auth_headers() -> dict[str, str]:
    """Build request headers, attaching a GITHUB_TOKEN if available to raise rate limits."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "CareerOS-Backend",
    }
    token: Optional[str] = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def fetch_repository_info(repo_url: str) -> RepoResponse:
    """
    Fetch repository metadata + language breakdown from GitHub and
    return it as a validated RepoResponse.
    """
    owner, repo = parse_github_url(repo_url)
    headers = _auth_headers()

    async with httpx.AsyncClient(timeout=10.0) as client:
        repo_resp = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}", headers=headers
        )

        if repo_resp.status_code == 404:
            raise GitHubServiceError(
                f"Repository '{owner}/{repo}' not found or is private.",
                status_code=404,
            )
        if repo_resp.status_code == 403:
            raise GitHubServiceError(
                "GitHub API rate limit exceeded. Add a GITHUB_TOKEN to increase limits.",
                status_code=429,
            )
        if repo_resp.status_code != 200:
            raise GitHubServiceError(
                f"GitHub API returned an unexpected error ({repo_resp.status_code}).",
                status_code=502,
            )

        repo_data = repo_resp.json()

        # Language breakdown (bytes of code per language) — best-effort, non-fatal.
        languages: dict[str, int] = {}
        try:
            lang_resp = await client.get(
                repo_data.get("languages_url", ""), headers=headers
            )
            if lang_resp.status_code == 200:
                languages = lang_resp.json()
        except httpx.HTTPError:
            languages = {}

        # README presence check — best-effort, non-fatal.
        has_readme = False
        try:
            readme_resp = await client.get(
                f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme", headers=headers
            )
            has_readme = readme_resp.status_code == 200
        except httpx.HTTPError:
            has_readme = False

    license_info = repo_data.get("license") or {}

    return RepoResponse(
        repo_name=repo_data.get("name", repo),
        full_name=repo_data.get("full_name", f"{owner}/{repo}"),
        owner=owner,
        description=repo_data.get("description"),
        url=repo_data.get("html_url", f"https://github.com/{owner}/{repo}"),
        homepage=repo_data.get("homepage") or None,
        primary_language=repo_data.get("language"),
        languages=languages,
        topics=repo_data.get("topics", []) or [],
        stars=repo_data.get("stargazers_count", 0),
        forks=repo_data.get("forks_count", 0),
        watchers=repo_data.get("watchers_count", 0),
        open_issues=repo_data.get("open_issues_count", 0),
        license=license_info.get("name"),
        default_branch=repo_data.get("default_branch", "main"),
        size_kb=repo_data.get("size", 0),
        is_fork=repo_data.get("fork", False),
        is_archived=repo_data.get("archived", False),
        visibility=repo_data.get("visibility", "public"),
        created_at=repo_data.get("created_at"),
        updated_at=repo_data.get("updated_at"),
        pushed_at=repo_data.get("pushed_at"),
        has_readme=has_readme,
    )