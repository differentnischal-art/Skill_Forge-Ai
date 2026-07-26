"""
GitHub data-fetching service.

Talks to the GitHub REST API only. Contains zero AI / prompting logic —
per system_design.md this layer's only job is to normalize GitHub data
into a clean shape. Feature extraction / prompt-building comes later.
"""

import base64
import os
from typing import Optional

import httpx

from api.schemas import RepoResponse, RepoSummary
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
    Fetch full repository metadata + language breakdown from GitHub for a
    single repo and return it as a validated RepoResponse.
    """
    owner, repo = parse_github_url(repo_url)
    headers = _auth_headers()

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
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

        languages: dict[str, int] = {}
        try:
            lang_resp = await client.get(
                repo_data.get("languages_url", ""), headers=headers
            )
            if lang_resp.status_code == 200:
                languages = lang_resp.json()
        except httpx.HTTPError:
            languages = {}

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


async def fetch_user_repos(username: str) -> list[RepoSummary]:
    """
    Fetch all public repos for a GitHub user (paginated, 100 per page).
    Powers the "list all repos after login" screen.
    """
    headers = _auth_headers()
    all_repos: list[RepoSummary] = []
    page = 1

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        while True:
            resp = await client.get(
                f"{GITHUB_API_BASE}/users/{username}/repos",
                headers=headers,
                params={"per_page": 100, "page": page, "sort": "updated"},
            )

            if resp.status_code == 404:
                raise GitHubServiceError(
                    f"GitHub user '{username}' not found.", status_code=404
                )
            if resp.status_code == 403:
                raise GitHubServiceError(
                    "GitHub API rate limit exceeded. Add a GITHUB_TOKEN to increase limits.",
                    status_code=429,
                )
            if resp.status_code != 200:
                raise GitHubServiceError(
                    f"GitHub API returned an unexpected error ({resp.status_code}).",
                    status_code=502,
                )

            batch = resp.json()
            if not batch:
                break

            for r in batch:
                all_repos.append(
                    RepoSummary(
                        repo_name=r["name"],
                        full_name=r["full_name"],
                        description=r.get("description"),
                        url=r["html_url"],
                        primary_language=r.get("language"),
                        stars=r.get("stargazers_count", 0),
                        forks=r.get("forks_count", 0),
                        updated_at=r.get("updated_at"),
                    )
                )

            page += 1

    return all_repos


async def fetch_readme_content(owner: str, repo: str) -> Optional[str]:
    """
    Fetch and decode the raw README text for a repo, if one exists.
    Returns None if there's no README (never raises for this case —
    a missing README is meaningful evidence, not an error).
    """
    headers = _auth_headers()

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        resp = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme", headers=headers
        )

        if resp.status_code == 404:
            return None
        if resp.status_code != 200:
            raise GitHubServiceError(
                f"Could not fetch README ({resp.status_code}).", status_code=502
            )

        data = resp.json()
        content_b64 = data.get("content", "")
        if not content_b64:
            return None

        try:
            decoded = base64.b64decode(content_b64).decode("utf-8", errors="replace")
        except Exception:
            return None

        max_chars = 6000
        if len(decoded) > max_chars:
            decoded = decoded[:max_chars] + "\n\n...[README truncated for length]..."

        return decoded


async def fetch_repo_file_tree(owner: str, repo: str, branch: str) -> list[dict]:
    """
    Fetch the full file tree of a repo via the Git Trees API.
    Returns a list of {"path": ..., "type": "blob"|"tree", "size": ...} dicts.
    Returns an empty list (not an error) if the repo is empty or the tree
    can't be read — an empty repo is meaningful evidence, not a failure.
    """
    headers = _auth_headers()

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        resp = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{branch}",
            headers=headers,
            params={"recursive": "1"},
        )

        if resp.status_code != 200:
            return []

        data = resp.json()
        return data.get("tree", [])


async def fetch_file_content(owner: str, repo: str, path: str, branch: str) -> Optional[str]:
    """
    Fetch and decode a single file's raw text content via the Contents API.
    Returns None on any failure (binary file, too large, deleted, etc.) —
    callers should skip files that return None rather than treat it as fatal.
    """
    headers = _auth_headers()

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            resp = await client.get(
                f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}",
                headers=headers,
                params={"ref": branch},
            )
        except httpx.HTTPError:
            return None

        if resp.status_code != 200:
            return None

        data = resp.json()

        if isinstance(data, list):
            return None  # path was a directory, not a file

        content_b64 = data.get("content", "")
        if not content_b64:
            return None

        try:
            return base64.b64decode(content_b64).decode("utf-8", errors="replace")
        except Exception:
            return None