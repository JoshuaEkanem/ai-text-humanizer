"""
core.py - Humanization engine for ai-text-humanizer
Communicates with a locally running Ollama instance.
"""

import requests
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2:3b"

PROMPT_TEMPLATE = """You are a writing assistant that rewrites AI-generated text to sound natural and human.

Rules:
- Use contractions where appropriate (e.g. "it's", "don't", "you'll")
- Vary sentence length — mix short punchy sentences with longer ones
- Avoid robotic or overly formal phrasing
- Keep the original meaning and all key information intact
- Do not add new information or opinions
- Return ONLY the rewritten text, no explanations or commentary

Text to rewrite:
{text}

Rewritten version:"""


def humanize(text: str, model: str = DEFAULT_MODEL) -> str:
    """
    Send text to a local Ollama model and return a humanized version.

    Args:
        text: The AI-generated text to rewrite.
        model: The Ollama model to use (default: llama3.2:3b).

    Returns:
        The humanized text as a string.

    Raises:
        ConnectionError: If Ollama is not running or unreachable.
        RuntimeError: If the model returns an unexpected response.
    """
    prompt = PROMPT_TEMPLATE.format(text=text.strip())

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,  # 2 min timeout — local models can be slow
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
