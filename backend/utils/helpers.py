"""
Small, dependency-free utility helpers.
Kept separate from services/ so parsing logic is easy to unit test on its own.
"""

import re

_GITHUB_URL_PATTERN = re.compile(
    r"^(?:https?://)?(?:www\.)?(?:github\.com/)?"
    r"(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)"
    r"(?:\.git)?/?$"
)


def parse_github_url(raw_url: str) -> tuple[str, str]:
    """
    Extract (owner, repo) from a GitHub URL or 'owner/repo' shorthand.

    Raises:
        ValueError: if the input doesn't match a recognizable GitHub repo pattern.
    """
    cleaned = raw_url.strip()
    match = _GITHUB_URL_PATTERN.match(cleaned)

    if not match:
        raise ValueError(
            f"'{raw_url}' is not a valid GitHub repository URL. "
            "Expected format: https://github.com/owner/repo"
        )

    owner = match.group("owner")
    repo = match.group("repo")

    if owner.lower() == "github.com" or not owner or not repo:
        raise ValueError(f"Could not extract owner/repo from '{raw_url}'")

    return owner, repo