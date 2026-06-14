"""
core.py - Humanization engine for ai-text-humanizer
Communicates with a locally running Ollama instance.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2:3b"

# Valid options
TONES = ["casual", "professional", "academic"]
INTENSITIES = ["light", "moderate", "heavy"]

# Tone descriptions injected into the prompt
TONE_INSTRUCTIONS = {
    "casual": (
        "The tone should be casual and conversational — like texting a friend. "
        "Use contractions freely, simple words, and a relaxed rhythm."
    ),
    "professional": (
        "The tone should be professional but natural — suitable for a work email or report. "
        "Use contractions where appropriate, avoid jargon, and keep it polished but not stiff."
    ),
    "academic": (
        "The tone should be academic but readable — suitable for a research paper or essay. "
        "Keep it structured and precise, but remove robotic or overly formulaic phrasing."
    ),
}

# Intensity instructions injected into the prompt
INTENSITY_INSTRUCTIONS = {
    "light": (
        "Make only minor adjustments — fix obviously robotic phrases, "
        "add a contraction or two, but keep most of the original wording intact."
    ),
    "moderate": (
        "Do a balanced rewrite — rephrase robotic sentences, vary the rhythm, "
        "and make it sound natural without straying too far from the original."
    ),
    "heavy": (
        "Fully transform the text — rewrite it from scratch in your own words "
        "while preserving all the original meaning and key information. "
        "Maximum humanization."
    ),
}

PROMPT_TEMPLATE = """You are a writing assistant that rewrites AI-generated text to sound natural and human.

Tone: {tone_instruction}

Rewrite intensity: {intensity_instruction}

Additional rules:
- Keep the original meaning and all key information intact
- Do not add new information or opinions
- Return ONLY the rewritten text, no explanations, labels, or commentary

Text to rewrite:
{text}

Rewritten version:"""


def build_prompt(text: str, tone: str, intensity: str) -> str:
    """Build a prompt string from text, tone, and intensity settings."""
    return PROMPT_TEMPLATE.format(
        tone_instruction=TONE_INSTRUCTIONS[tone],
        intensity_instruction=INTENSITY_INSTRUCTIONS[intensity],
        text=text.strip(),
    )


def humanize(
    text: str,
    model: str = DEFAULT_MODEL,
    tone: str = "professional",
    intensity: str = "moderate",
) -> str:
    """
    Send text to a local Ollama model and return a humanized version.

    Args:
        text: The AI-generated text to rewrite.
        model: The Ollama model to use (default: llama3.2:3b).
        tone: Output tone — 'casual', 'professional', or 'academic'.
        intensity: Rewrite intensity — 'light', 'moderate', or 'heavy'.

    Returns:
        The humanized text as a string.

    Raises:
        ValueError: If tone or intensity is invalid.
        ConnectionError: If Ollama is not running or unreachable.
        RuntimeError: If the model returns an unexpected response.
    """
    if tone not in TONES:
        raise ValueError(f"Invalid tone '{tone}'. Choose from: {', '.join(TONES)}")
    if intensity not in INTENSITIES:
        raise ValueError(f"Invalid intensity '{intensity}'. Choose from: {', '.join(INTENSITIES)}")

    prompt = build_prompt(text, tone, intensity)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Could not connect to Ollama. Make sure it is running (try: ollama serve)"
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("Ollama took too long to respond. Try a smaller model.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Ollama returned an error: {e}")

    data = response.json()

    if "response" not in data:
        raise RuntimeError(f"Unexpected response from Ollama: {data}")

    return data["response"].strip()


def check_ollama_connection(model: str = DEFAULT_MODEL) -> bool:
    """
    Verify that Ollama is running and the requested model is available.

    Returns:
        True if the connection is healthy, False otherwise.
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        models = [m["name"] for m in response.json().get("models", [])]
        return any(model.split(":")[0] in m for m in models)
    except Exception:
        return False
