"""
JWT creation and verification for session handling.
Kept separate from the API layer — routes call these functions,
never touch jwt.encode/decode directly.
"""

import os
from datetime import datetime, timedelta, timezone

import jwt

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class TokenError(Exception):
    """Raised when a token is invalid, expired, or malformed."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def _get_secret_key() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError(
            "JWT_SECRET_KEY is not set in the environment. Add it to backend/.env"
        )
    return secret


def create_access_token(user_id: int, github_id: int, username: str) -> str:
    """Creates a signed JWT encoding the user's identity, valid for 7 days."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "github_id": github_id,
        "username": username,
        "exp": expire,
    }
    return jwt.encode(payload, _get_secret_key(), algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Verifies and decodes a JWT. Raises TokenError if invalid/expired."""
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenError("Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise TokenError("Invalid session token.")