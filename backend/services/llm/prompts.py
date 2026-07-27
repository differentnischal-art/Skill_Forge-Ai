"""
Prompt templates for LLM calls.
Kept separate from the API client so prompt text can be versioned
independently of how it's sent (see prompt_library.md's own rule on this).

Implements:
- Prompt 4 (Repository Reviewer) — single-repo feedback
- Prompt 1 (Career Analysis) — whole-profile guidance
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
If evidence is unavailable, explicitly state that clearly.

RULES ABOUT CODE QUALITY:
- You will be given either (a) real source code excerpts from the repository, or (b) a note that no source code excerpts were available.
- If real source code excerpts ARE provided below, base code_quality_estimate ONLY on what you can actually observe in those excerpts: naming, structure, error handling, comments, obvious bugs, etc. Be specific and cite what you saw.
- If NO source code excerpts are provided, code_quality_estimate MUST be exactly: "Cannot be assessed — no source code was available to review, only metadata and README text."
- Never infer code quality from the README's description of what the project claims to do. The README is the author's claim, not verified evidence.

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
    code_samples_text: str = "",
    files_reviewed: list[str] | None = None,
    total_source_files_found: int = 0,
) -> str:
    """
    Builds the user-turn prompt for Prompt 4 (Repository Reviewer),
    including real source code excerpts when available.
    """
    files_reviewed = files_reviewed or []

    description_text = description if description else "No description provided."
    language_text = primary_language if primary_language else "Not detected."
    languages_text = ", ".join(languages.keys()) if languages else "None detected."
    topics_text = ", ".join(topics) if topics else "None."
    readme_text = (
        readme_content if readme_content else "No README file exists in this repository."
    )

    if code_samples_text.strip():
        code_section = f"""Source Code Excerpts (from {len(files_reviewed)} of {total_source_files_found} total source files found):
{code_samples_text}"""
    else:
        code_section = (
            f"No source code excerpts are available for review. "
            f"({total_source_files_found} source files were found in the repository, "
            f"but none could be fetched or none exist.)"
        )

    return f"""Review the following repository.

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

{code_section}

Analyze this repository and return ONLY a JSON object with exactly this structure:

{{
  "repo_purpose": "one or two sentences on what this repository does, based on all evidence above",
  "code_quality_estimate": "assessment based ONLY on actual code excerpts if provided, otherwise the fixed 'cannot be assessed' string",
  "documentation_quality": "assessment of the README/description quality, or explicit note if missing",
  "suggested_improvements": ["specific, actionable improvement 1", "specific, actionable improvement 2"],
  "missing_evidence_notes": ["explicit note about any information that could not be evaluated due to missing data"]
}}

Rules:
- Use only the evidence provided above. Do not assume technologies, features, or quality not shown in the data.
- If code excerpts were provided, cite specific observations rather than vague praise or criticism.
- If description or README is missing, say so explicitly in missing_evidence_notes.
- Every suggested improvement must be specific and actionable, not generic advice like "write better code".
- Return ONLY the JSON object, nothing else.
"""


CAREER_ANALYSIS_SYSTEM_PROMPT = """You are an experienced Senior Software Engineer, Technical Mentor, and Career Coach.

Your responsibility is to analyze engineering students based on evidence rather than assumptions.
Never exaggerate a student's skills. Never invent missing information.
If evidence is unavailable, explicitly state that.
Always encourage project-based learning instead of passive learning.
Focus on helping the student become industry-ready.

RULE ABOUT THE STATED CAREER GOAL:
This platform is scoped to software engineering, data science, and technology-related careers only.
If the stated career goal is NOT a recognizable software engineering, data science, or technology-related role (e.g. it names a non-technical profession like "cook", "doctor", "lawyer", or is nonsensical/empty), you MUST NOT reinterpret or force-fit it into a technology context.
Instead, set "career_readiness" to "Not applicable" and explain clearly in "overall_summary" that the stated goal does not appear to be a technology-related career, and that this platform's analysis is designed for software/tech roles. In this case, "strengths", "weaknesses", and "missing_skills" should reflect only what is genuinely observable from the repos in general terms, without inventing a fictional connection to the unrelated goal.

You must always respond with valid JSON only. No markdown formatting, no code fences, no preamble.
"""


def build_career_analysis_prompt(
    career_goal: str,
    profile_summary: str,
    repositories_block: str,
    technologies_block: str,
) -> str:
    """Implements Prompt 1 (Career Analysis) from prompt_library.md."""
    return f"""Analyze the student's GitHub profile.

Career Goal:
{career_goal}

Profile Summary:
{profile_summary}

Repositories:
{repositories_block}

Technologies:
{technologies_block}

Return ONLY a JSON object with exactly this structure:

{{
  "strengths": ["specific strength grounded in the repos above"],
  "weaknesses": ["specific weakness grounded in the repos above"],
  "missing_skills": ["skill missing relative to the stated career goal"],
  "career_readiness": "High, Medium, Low, or Not applicable, with a one-sentence justification",
  "overall_summary": "2-3 sentence honest summary"
}}

Rules:
- Use only the evidence provided above. Never hallucinate repositories or skills not shown.
- Every weakness must be explained with reference to what's missing or present in the data.
- Avoid generic advice — tie everything to the actual repos listed.
- If the career goal is not a recognizable technology-related role, follow the system prompt's rule about that exactly — do not invent a technology interpretation of it.
- Return ONLY the JSON object, nothing else.
"""