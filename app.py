"""
app.py - Flask web interface for ai-text-humanizer (Phase 4)

Usage:
    python app.py
    Then open http://localhost:5000 in your browser.
"""

import time
from flask import Flask, render_template, request, jsonify
from humanizer.core import humanize, check_ollama_connection, DEFAULT_MODEL, TONES, INTENSITIES

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main UI page."""
    return render_template(
        "index.html",
        tones=TONES,
        intensities=INTENSITIES,
        default_tone="professional",
        default_intensity="moderate",
    )


@app.route("/humanize", methods=["POST"])
def humanize_text():
    """
    API endpoint that accepts JSON and returns humanized text.

    Expected request body:
        {
            "text": "...",
            "tone": "casual" | "professional" | "academic",
            "intensity": "light" | "moderate" | "heavy"
        }

    Returns:
        {
            "result": "...",
            "tone": "...",
            "intensity": "...",
            "elapsed": 4.2
        }
    """
    data = request.get_json()

    text = (data.get("text") or "").strip()
    tone = data.get("tone", "professional")
    intensity = data.get("intensity", "moderate")

    if not text:
        return jsonify({"error": "No text provided."}), 400

    if tone not in TONES:
        return jsonify({"error": f"Invalid tone. Choose from: {', '.join(TONES)}"}), 400

    if intensity not in INTENSITIES:
        return jsonify({"error": f"Invalid intensity. Choose from: {', '.join(INTENSITIES)}"}), 400

    try:
        start = time.time()
        result = humanize(text, model=DEFAULT_MODEL, tone=tone, intensity=intensity)
        elapsed = round(time.time() - start, 1)
        return jsonify({"result": result, "tone": tone, "intensity": intensity, "elapsed": elapsed})
    except ConnectionError as e:
        return jsonify({"error": str(e)}), 503
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """Quick health check — confirms Ollama is reachable."""
    ok = check_ollama_connection(DEFAULT_MODEL)
    status = "ok" if ok else "ollama_unavailable"
    return jsonify({"status": status}), 200 if ok else 503


if __name__ == "__main__":
    print("\n AI Text Humanizer — Web UI")
    print(" Open http://localhost:5000 in your browser\n")
    app.run(debug=False, port=5000)
