"""
API layer — thin HTTP wrapper. No business logic lives here.
"""

from fastapi import APIRouter, HTTPException

from api.schemas import (
    CareerAnalysisRequest,
    CareerAnalysisResponse,
    RepoAnalyzeRequest,
    RepoResponse,
)
from services.analyzer.profile_analyzer import (
    build_profile_summary,
    build_repositories_block,
    build_technologies_block,
)
from services.github.github_api import (
    fetch_repository_info,
    fetch_user_repos,
    GitHubServiceError,
)
from services.llm.gemini_client import call_gemini_json, LLMServiceError
from services.llm.prompts import (
    build_career_analysis_prompt,
    CAREER_ANALYSIS_SYSTEM_PROMPT,
)

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=RepoResponse)
async def analyze_repository(payload: RepoAnalyzeRequest) -> RepoResponse:
    """Single-repo raw metadata. No AI here — Step 1 scope."""
    try:
        return await fetch_repository_info(payload.repo_url)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/career-analysis", response_model=CareerAnalysisResponse)
async def career_analysis(payload: CareerAnalysisRequest) -> CareerAnalysisResponse:
    """
    Whole-profile career guidance (Prompt 1). Fetches all repos for a user,
    builds a curated summary (never raw JSON), and asks the LLM for
    strengths/weaknesses/missing_skills relative to the stated career goal.
    """
    try:
        repos = await fetch_user_repos(payload.username)

        profile_summary = build_profile_summary(payload.username, repos)
        repositories_block = build_repositories_block(repos)
        technologies_block = build_technologies_block(repos)

        user_prompt = build_career_analysis_prompt(
            career_goal=payload.career_goal,
            profile_summary=profile_summary,
            repositories_block=repositories_block,
            technologies_block=technologies_block,
        )

        ai_result = call_gemini_json(CAREER_ANALYSIS_SYSTEM_PROMPT, user_prompt)

        return CareerAnalysisResponse(
            strengths=ai_result.get("strengths", []),
            weaknesses=ai_result.get("weaknesses", []),
            missing_skills=ai_result.get("missing_skills", []),
            career_readiness=ai_result.get("career_readiness", ""),
            overall_summary=ai_result.get("overall_summary", ""),
            repos_analyzed=len(repos),
        )

    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except LLMServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc