# AI Text Humanizer

A lightweight, fully offline tool that rewrites AI-generated text to sound more natural and human. Built on top of [Ollama](https://ollama.com) for local LLM inference — no internet connection or API keys required after setup.

> **Status:** Phase 1 — CLI Engine ✅

---

## Features (Phase Roadmap)

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Core engine + CLI | ✅ Done |
| 2 | Prompt engineering (tone/intensity controls) | ✅ Done |
| 3 | Flask web UI | ✅ Done |
| 4 | UI polish + diff view | 🔜 Planned |
| 5 | PyInstaller Windows executable | ⬜ Planned |

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/download) installed and running
- A pulled Ollama model (default: `llama3.2:3b`)

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/ai-text-humanizer.git
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

**Run the CLI:**
```bash
python cli.py
```

**Use a different model:**
```bash
python cli.py --model mistral:7b
```

Paste your AI-generated text, press **Enter twice**, and the tool returns a humanized version.

---

## How It Works

1. The CLI sends your text to a locally running Ollama instance via its REST API (`localhost:11434`).
2. A carefully engineered prompt instructs the model to rewrite the text — using contractions, varying sentence rhythm, and removing robotic phrasing — without changing the original meaning.
3. The result is printed directly in the terminal.

All processing happens on your machine. No data leaves your device.

---

## Project Structure

```
ai-text-humanizer/
├── cli.py              # CLI entry point
├── requirements.txt
├── README.md
└── humanizer/
    ├── __init__.py
    └── core.py         # humanize() function and Ollama API calls
```

---

## License

MIT
