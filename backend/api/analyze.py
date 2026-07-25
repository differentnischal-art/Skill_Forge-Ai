"""
API layer — thin HTTP wrapper around services/github_service.py.
No business logic lives here; only request/response handling.
"""

from fastapi import APIRouter, HTTPException

from models.schemas import RepoAnalyzeRequest, RepoResponse
from services.github_service import fetch_repository_info, GitHubServiceError

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=RepoResponse)
async def analyze_repository(payload: RepoAnalyzeRequest) -> RepoResponse:
    """
    Accepts a GitHub repository URL and returns structured repository
    metadata as JSON. This is Step 1 only — no AI analysis happens here.
    """
    try:
        return await fetch_repository_info(payload.repo_url)
    except ValueError as exc:
        # Bad / unparseable URL
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc