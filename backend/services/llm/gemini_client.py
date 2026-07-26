"""
Thin wrapper around the Google Gemini API.
No prompt text lives here — only the mechanics of calling Gemini and
parsing its JSON response. Prompt content lives in services/llm/prompts.py.
"""

import json
import os

import google.generativeai as genai

MODEL_NAME = "gemini-3.1-flash-lite"


class LLMServiceError(Exception):
    """Raised when the LLM call fails or returns unusable output."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _get_model(system_prompt: str) -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise LLMServiceError(
            "GEMINI_API_KEY is not set in the environment.", status_code=500
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=system_prompt,
    )


def call_gemini_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Calls Gemini with a system + user prompt, expecting a JSON object back.
    Raises LLMServiceError on API failure or invalid JSON.
    """
    try:
        model = _get_model(system_prompt)
        response = model.generate_content(
            user_prompt,
            generation_config={
                "temperature": 0.4,
                "response_mime_type": "application/json",
            },
        )
    except Exception as exc:
        raise LLMServiceError(f"Gemini API error: {exc}", status_code=502) from exc

    raw_text = (response.text or "").strip()

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