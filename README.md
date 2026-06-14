# AI Text Humanizer

A lightweight, fully offline tool that rewrites AI-generated text to sound more natural and human. Built on top of [Ollama](https://ollama.com) for local LLM inference — no internet connection or API keys required after setup.

> **Status:** All phases complete ✅

---

## Features (Phase Roadmap)

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Core engine + CLI | ✅ Done |
| 2 | Prompt engineering (tone/intensity controls) | ✅ Done |
| 3 | Flask web UI | ✅ Done |
| 4 | UI polish + diff view | ✅ Done |
| 5 | PyInstaller Windows executable | ✅ Done |

---

## Key Features

- **Fully offline** — no API keys, no internet required after setup
- **Tone control** — casual, professional, or academic output
- **Intensity control** — light touch, balanced, or full rewrite
- **Diff view** — side-by-side comparison of original vs humanized text
- **Word & character counts** — live input and output counters
- **Processing time** — shows how long each rewrite took
- **CLI + Web UI** — use whichever suits your workflow
- **Standalone .exe** — run on any Windows machine without Python

---

## Requirements

- Python 3.9+ (for running from source)
- [Ollama](https://ollama.com/download) installed and running
- A pulled Ollama model (default: `llama3.2:3b`)

---

## Setup (Run from Source)

**1. Clone the repo**
```bash
git clone https://github.com/JoshuaEkanem/ai-text-humanizer.git
cd ai-text-humanizer
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Pull a model via Ollama**
```bash
ollama pull llama3.2:3b
```

---

## Usage

**Web UI (recommended):**
```bash
python app.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

**CLI:**
```bash
python cli.py
```

**CLI with a different model:**
```bash
python cli.py --model mistral:7b
```

---

## Build Windows Executable

```bash
pip install pyinstaller
pyinstaller humanizer.spec
```

The `.exe` will be output to `dist/AI-Text-Humanizer.exe`. Double-click to run — it starts Flask in the background and opens your browser automatically.

> **Note:** Ollama must be installed and running on the target machine.

---

## How It Works

1. Your text is sent to a locally running Ollama instance via its REST API (`localhost:11434`).
2. A prompt engineered for tone and intensity instructs the model to rewrite the text — using contractions, varying sentence rhythm, and removing robotic phrasing — without changing the original meaning.
3. The result is returned with a word-level diff highlighting what changed.

All processing happens on your machine. No data leaves your device.

---

## Project Structure

```
ai-text-humanizer/
├── launcher.py         # PyInstaller entry point (auto-opens browser)
├── app.py              # Flask app and API routes
├── cli.py              # CLI entry point
├── humanizer.spec      # PyInstaller build config
├── requirements.txt
├── README.md
├── humanizer/
│   ├── __init__.py
│   └── core.py         # humanize() function and Ollama API calls
└── templates/
    └── index.html      # Web UI
```

---

## License

MIT
