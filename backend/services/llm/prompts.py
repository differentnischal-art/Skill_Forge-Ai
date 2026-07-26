"""
Prompt templates for LLM calls.
Kept separate from the API client so prompt text can be versioned
independently of how it's sent (see prompt_library.md's own rule on this).

This module implements Prompt 4 (Repository Reviewer) from prompt_library.md.
"""

REPOSITORY_REVIEWER_SYSTEM_PROMPT = """You are an experienced Senior Software Engineer, Technical Mentor, and Career Coach.

Your responsibility is to analyze engineering students based on evidence rather than assumptions.

Your recommendations must always be:
- Personalized
- Practical
- Actionable
- Honest
- Explainable

Never exaggerate a student's skills.
Never invent missing information.
If evidence is unavailable, explicitly state that clearly (e.g. "No description was provided, so the repository's purpose is unclear from GitHub metadata alone.").
Always encourage project-based learning instead of passive learning.
Focus on helping the student become industry-ready.

You must always respond with valid JSON only. No markdown formatting, no code fences, no preamble or explanation outside the JSON object.
"""


def build_repository_reviewer_prompt(
    repo_name: str,
    description: str | None,
    primary_language: str | None,
    languages: dict[str, int],
    topics: list[str],
    stars: int,
    forks: int,
    has_readme: bool,
    readme_content: str | None,
) -> str:
    """
    Builds the user-turn prompt for Prompt 4 (Repository Reviewer).
    Only real, fetched data is interpolated — never invented values.
    """
    description_text = description if description else "No description provided."
    language_text = primary_language if primary_language else "Not detected."
    languages_text = ", ".join(languages.keys()) if languages else "None detected."
    topics_text = ", ".join(topics) if topics else "None."
    readme_text = (
        readme_content if readme_content else "No README file exists in this repository."
    )

    return f"""Review the following repository metadata.

Repository Name:
{repo_name}

Description:
{description_text}

Primary Language:
{language_text}

All Detected Languages:
{languages_text}

Topics:
{topics_text}

Stars: {stars}
Forks: {forks}
Has README: {has_readme}

README Content:
{readme_text}

Analyze this repository and return ONLY a JSON object with exactly this structure:

{{
  "repo_purpose": "one or two sentences on what this repository does, based only on the evidence above",
  "code_quality_estimate": "High, Medium, or Low, with a one-sentence justification based on available evidence",
  "documentation_quality": "assessment of the README/description quality, or explicit note if missing",
  "suggested_improvements": ["specific, actionable improvement 1", "specific, actionable improvement 2"],
  "missing_evidence_notes": ["explicit note about any information that could not be evaluated due to missing data"]
}}

Rules:
- Use only the evidence provided above. Do not assume technologies, features, or quality not shown in the data.
- If description or README is missing, say so explicitly in missing_evidence_notes.
- Every suggested improvement must be specific and actionable, not generic advice like "write better code".
- Return ONLY the JSON object, nothing else.
"""