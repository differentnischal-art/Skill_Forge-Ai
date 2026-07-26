"""
Thin wrapper around the Anthropic API.
No prompt text lives here — only the mechanics of calling Claude and
parsing its JSON response. Prompt content lives in services/llm/prompts.py.
"""

import json
import os

from anthropic import Anthropic, APIError

MODEL = "claude-sonnet-5"
MAX_TOKENS = 1500


class LLMServiceError(Exception):
    """Raised when the LLM call fails or returns unusable output."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _get_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMServiceError(
            "ANTHROPIC_API_KEY is not set in the environment.", status_code=500
        )
    return Anthropic(api_key=api_key)


def call_claude_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Calls Claude with a system + user prompt, expecting a JSON object back.
    Raises LLMServiceError on API failure or invalid JSON.
    """
    client = _get_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except APIError as exc:
        raise LLMServiceError(f"Anthropic API error: {exc}", status_code=502) from exc

    text_blocks = [block.text for block in response.content if block.type == "text"]
    raw_text = "".join(text_blocks).strip()

    # Defensive cleanup in case the model wraps output in markdown fences anyway.
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise LLMServiceError(
            f"LLM did not return valid JSON. Raw output: {raw_text[:300]}",
            status_code=502,
        ) from exc