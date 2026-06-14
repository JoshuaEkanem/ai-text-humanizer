"""
cli.py - Command-line interface for ai-text-humanizer (Phase 1)

Usage:
    python cli.py                  # interactive mode (paste text, press Enter twice)
    python cli.py --model mistral  # use a different Ollama model
"""

import argparse
import sys
from humanizer.core import humanize, check_ollama_connection, DEFAULT_MODEL


BANNER = """
╔══════════════════════════════════════╗
║       AI Text Humanizer v0.1         ║
║       Phase 1 — CLI Engine           ║
╚══════════════════════════════════════╝
"""


def get_multiline_input(prompt: str) -> str:
    """Read multiple lines of input until the user enters a blank line."""
    print(prompt)
    print("(Paste your text below. Press Enter twice when done)\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser(
        description="Humanize AI-generated text using a local Ollama model."
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    print(BANNER)

    # Pre-flight check
    print(f"Checking Ollama connection (model: {args.model})...")
    if not check_ollama_connection(args.model):
        print(
            f"\n[ERROR] Could not reach Ollama or model '{args.model}' is not available.\n"
            f"  - Make sure Ollama is running: ollama serve\n"
            f"  - Make sure the model is pulled: ollama pull {args.model}\n"
        )
        sys.exit(1)
    print("Ollama is running. Ready.\n")

    # Main loop
    while True:
        try:
            text = get_multiline_input("--- INPUT ---")

            if not text:
                print("[Skipped — no text entered]\n")
                continue

            print("\nHumanizing... please wait.\n")

            result = humanize(text, model=args.model)

            print("--- OUTPUT ---")
            print(result)
            print("-" * 40)

            again = input("\nHumanize another? (y/n): ").strip().lower()
            if again != "y":
                print("\nDone. Exiting.")
                break
            print()

        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting.")
            break
        except (ConnectionError, RuntimeError) as e:
            print(f"\n[ERROR] {e}\n")
            break


if __name__ == "__main__":
    main()
