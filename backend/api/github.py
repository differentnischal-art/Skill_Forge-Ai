"""
API layer for GitHub user/profile-level endpoints and AI repository feedback.
Thin HTTP wrapper only — no business logic here.
"""

from fastapi import APIRouter, HTTPException

from api.schemas import FeedbackRequest, FeedbackResponse, RepoSummary
from services.analyzer.code_quality import collect_code_samples
from services.github.github_api import (
    fetch_readme_content,
    fetch_repository_info,
    fetch_user_repos,
    GitHubServiceError,
)
from services.llm.gemini_client import call_gemini_json, LLMServiceError
from services.llm.prompts import (
    build_repository_reviewer_prompt,
    REPOSITORY_REVIEWER_SYSTEM_PROMPT,
)
from utils.helpers import parse_github_url

router = APIRouter(prefix="/api/github", tags=["github"])


@router.get("/repos/{username}", response_model=list[RepoSummary])
async def list_user_repos(username: str) -> list[RepoSummary]:
    """
    Returns all public repos for a GitHub user.
    Powers the repo-list screen shown right after login.
    """
    try:
        return await fetch_user_repos(username)
    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/feedback", response_model=FeedbackResponse)
async def get_repository_feedback(payload: FeedbackRequest) -> FeedbackResponse:
    """
    Fetches a repo's real metadata + README + representative source code
    samples, then asks Gemini to proactively review it (Prompt 4: Repository
    Reviewer). Raw stats are always included; AI feedback happens regardless
    of whether the user explicitly asks for it.
    """
    try:
        owner, repo = parse_github_url(payload.repo_url)
        repo_info = await fetch_repository_info(payload.repo_url)
        readme_content = await fetch_readme_content(owner, repo)
        code_samples = await collect_code_samples(owner, repo, repo_info.default_branch)

        user_prompt = build_repository_reviewer_prompt(
            repo_name=repo_info.repo_name,
            description=repo_info.description,
            primary_language=repo_info.primary_language,
            languages=repo_info.languages,
            topics=repo_info.topics,
            stars=repo_info.stars,
            forks=repo_info.forks,
            has_readme=repo_info.has_readme,
            readme_content=readme_content,
            code_samples_text=code_samples["combined_code_text"],
            files_reviewed=code_samples["files_reviewed"],
            total_source_files_found=code_samples["total_source_files_found"],
        )

        ai_result = call_gemini_json(REPOSITORY_REVIEWER_SYSTEM_PROMPT, user_prompt)

        return FeedbackResponse(
            repo_purpose=ai_result.get("repo_purpose", ""),
            code_quality_estimate=ai_result.get("code_quality_estimate", ""),
            documentation_quality=ai_result.get("documentation_quality", ""),
            suggested_improvements=ai_result.get("suggested_improvements", []),
            missing_evidence_notes=ai_result.get("missing_evidence_notes", []),
            files_reviewed=code_samples["files_reviewed"],
            total_source_files_found=code_samples["total_source_files_found"],
            raw_stats=repo_info,
        )

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except LLMServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc