"""
GitHub OAuth login flow + JWT session handling.

Flow:
1. Frontend redirects browser to GET /api/auth/github/login
2. That redirects to GitHub's authorize page
3. GitHub redirects back to GET /api/auth/github/callback?code=...
4. Backend exchanges code -> GitHub access token -> fetches GitHub profile
5. Backend creates/updates User row, issues a JWT, redirects to frontend with it
"""

import os
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from api.schemas import UserResponse
from databases import crud
from databases.connection import get_db
from services.auth.jwt_handler import create_access_token, decode_access_token, TokenError
from services.github.github_api import (
    exchange_code_for_token,
    fetch_authenticated_github_user,
    GitHubServiceError,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()


@router.get("/github/login")
async def github_login():
    """Redirects the browser to GitHub's OAuth authorize page."""
    client_id = os.getenv("GITHUB_CLIENT_ID")
    redirect_uri = os.getenv("GITHUB_OAUTH_REDIRECT_URI")

    if not client_id or not redirect_uri:
        raise HTTPException(
            status_code=500,
            detail="GITHUB_CLIENT_ID or GITHUB_OAUTH_REDIRECT_URI not configured.",
        )

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "read:user repo",
    }
    github_authorize_url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url=github_authorize_url)


@router.get("/github/callback")
async def github_callback(
    code: str = Query(...), db: Session = Depends(get_db)
):
    """
    Handles GitHub's redirect back after the user approves login.
    Exchanges the code for a token, fetches the user's profile,
    saves/updates the User row, issues a JWT, and redirects to the frontend.
    """
    try:
        github_access_token = await exchange_code_for_token(code)
        github_user = await fetch_authenticated_github_user(github_access_token)

        user = crud.create_or_update_user(
            db=db,
            github_id=github_user["id"],
            username=github_user["login"],
            avatar_url=github_user.get("avatar_url"),
            bio=github_user.get("bio"),
        )

        jwt_token = create_access_token(
            user_id=user.id, github_id=user.github_id, username=user.username
        )

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        redirect_url = f"{frontend_url}/auth/callback?token={jwt_token}"
        return RedirectResponse(url=redirect_url)

    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    FastAPI dependency — extracts and verifies the JWT from the
    Authorization header, returns the corresponding User row.
    Use this on any route that requires a logged-in user.
    """
    try:
        payload = decode_access_token(credentials.credentials)
    except TokenError as exc:
        raise HTTPException(status_code=401, detail=exc.message) from exc

    user = crud.get_user_by_id(db, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    """Returns the currently logged-in user's profile, based on their JWT."""
    return UserResponse(
        id=current_user.id,
        github_id=current_user.github_id,
        username=current_user.username,
        avatar_url=current_user.avatar_url,
        bio=current_user.bio,
        career_goal=current_user.career_goal,
    )