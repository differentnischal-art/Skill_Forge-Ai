"""
Selects representative source files from a repo's file tree and fetches
their content, so the LLM can assess real code instead of just README claims.

This is intentionally conservative about size: we never want to send an
entire repository into a single LLM call, so we pick a small, meaningful
sample and cap total characters sent.
"""

from services.github.github_api import fetch_file_content, fetch_repo_file_tree

# Extensions considered "source code" worth reviewing.
CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rb", ".php",
    ".c", ".cpp", ".h", ".cs", ".rs", ".kt", ".swift", ".sql",
}

# Path fragments to always skip — dependency/build artifacts, not authored code.
SKIP_PATH_FRAGMENTS = (
    "node_modules/", "venv/", ".venv/", "__pycache__/", ".git/",
    "dist/", "build/", ".next/", "vendor/", "migrations/",
    "package-lock.json", "yarn.lock", "poetry.lock",
)

MAX_FILES = 5
MAX_CHARS_PER_FILE = 2500
MAX_TOTAL_CHARS = 10000


def _is_reviewable(path: str, file_type: str) -> bool:
    if file_type != "blob":
        return False
    if any(fragment in path for fragment in SKIP_PATH_FRAGMENTS):
        return False
    return any(path.endswith(ext) for ext in CODE_EXTENSIONS)


def _select_candidate_paths(tree: list[dict]) -> list[str]:
    """
    Pick up to MAX_FILES source file paths, preferring shorter/shallower
    paths first (usually entry points: main.py, app.js, index.ts, etc.)
    over deeply nested files.
    """
    candidates = [
        item["path"]
        for item in tree
        if _is_reviewable(item.get("path", ""), item.get("type", ""))
    ]
    candidates.sort(key=lambda p: (p.count("/"), len(p)))
    return candidates[:MAX_FILES]


async def collect_code_samples(owner: str, repo: str, branch: str) -> dict:
    """
    Returns:
        {
            "files_reviewed": ["path1", "path2", ...],
            "combined_code_text": "concatenated, capped source excerpts",
            "total_source_files_found": int,
        }
    A repo with no matching source files returns files_reviewed=[] and
    combined_code_text="" — this is real evidence (no code to review),
    not an error.
    """
    tree = await fetch_repo_file_tree(owner, repo, branch)
    reviewable = [
        item for item in tree if _is_reviewable(item.get("path", ""), item.get("type", ""))
    ]
    candidate_paths = _select_candidate_paths(tree)

    collected: list[str] = []
    files_reviewed: list[str] = []
    total_chars = 0

    for path in candidate_paths:
        if total_chars >= MAX_TOTAL_CHARS:
            break

        content = await fetch_file_content(owner, repo, path, branch)
        if content is None:
            continue

        snippet = content[:MAX_CHARS_PER_FILE]
        if len(content) > MAX_CHARS_PER_FILE:
            snippet += "\n...[truncated]..."

        remaining_budget = MAX_TOTAL_CHARS - total_chars
        if len(snippet) > remaining_budget:
            snippet = snippet[:remaining_budget] + "\n...[truncated]..."

        collected.append(f"### File: {path}\n{snippet}")
        files_reviewed.append(path)
        total_chars += len(snippet)

    return {
        "files_reviewed": files_reviewed,
        "combined_code_text": "\n\n".join(collected),
        "total_source_files_found": len(reviewable),
    }