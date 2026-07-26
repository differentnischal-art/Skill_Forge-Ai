"""
Aggregates a user's repo list into a compact profile summary suitable
for Prompt 1 (Career Analysis) — never sends raw GitHub JSON to the LLM,
only a curated summary (per system_design.md §12).
"""

from api.schemas import RepoSummary


def build_profile_summary(username: str, repos: list[RepoSummary]) -> str:
    """Human-readable summary of the user's overall GitHub activity."""
    if not repos:
        return f"GitHub user '{username}' has no public repositories."

    total = len(repos)
    with_description = sum(1 for r in repos if r.description)
    languages = {r.primary_language for r in repos if r.primary_language}

    return (
        f"GitHub user '{username}' has {total} public repositories. "
        f"{with_description} of {total} have a description. "
        f"Detected primary languages across repos: {', '.join(sorted(languages)) or 'none detected'}."
    )


def build_repositories_block(repos: list[RepoSummary]) -> str:
    """Compact per-repo listing — real data only, capped to keep prompt size sane."""
    lines = []
    for r in repos[:20]:  # cap to avoid oversized prompts on very active profiles
        desc = r.description if r.description else "No description provided."
        lang = r.primary_language if r.primary_language else "Not detected."
        lines.append(
            f"- {r.repo_name} | Language: {lang} | Stars: {r.stars} | "
            f"Updated: {r.updated_at} | Description: {desc}"
        )
    return "\n".join(lines)


def build_technologies_block(repos: list[RepoSummary]) -> str:
    """Distinct languages detected across all repos — real evidence only."""
    languages = sorted({r.primary_language for r in repos if r.primary_language})
    return ", ".join(languages) if languages else "No languages detected across repositories."