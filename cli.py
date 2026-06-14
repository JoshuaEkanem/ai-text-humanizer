"""
cli.py - Command-line interface for ai-text-humanizer (Phase 2)

Usage:
    python cli.py                  # interactive mode
    python cli.py --model mistral  # use a different Ollama model
"""

import argparse
import sys
from humanizer.core import (
    humanize,
    check_ollama_connection,
    DEFAULT_MODEL,
    TONES,
    INTENSITIES,
)


BANNER = """
╔══════════════════════════════════════╗
║       AI Text Humanizer v0.2         ║
║       Phase 2 — Prompt Engineering   ║
╚══════════════════════════════════════╝
"""


def get_multiline_input() -> str:
    """Read multiple lines of input until the user enters a blank line."""
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


def pick_option(label: str, options: list, default: str) -> str:
    """
    Display a numbered menu and return the user's choice.
    Pressing Enter without a selection returns the default.
    """
    print(f"\n{label}")
    for i, opt in enumerate(options, 1):
        marker = " (default)" if opt == default else ""
        print(f"  {i}. {opt}{marker}")

    while True:
        choice = input(f"Enter 1-{len(options)} or press Enter for default: ").strip()
        if choice == "":
            return default
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"  Please enter a number between 1 and {len(options)}.")


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
            # Step 1 — pick tone and intensity
            tone = pick_option("Tone:", TONES, default="professional")
            intensity = pick_option("Intensity:", INTENSITIES, default="moderate")

            # Step 2 — get input text
            print(f"\n--- INPUT  [tone: {tone} | intensity: {intensity}] ---")
            text = get_multiline_input()

            if not text:
                print("[Skipped — no text entered]\n")
                continue

            print("\nHumanizing... please wait.\n")

            # Step 3 — humanize
            result = humanize(text, model=args.model, tone=tone, intensity=intensity)

            # Step 4 — show output
            print(f"--- OUTPUT [tone: {tone} | intensity: {intensity}] ---")
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
        except (ConnectionError, RuntimeError, ValueError) as e:
            print(f"\n[ERROR] {e}\n")
            break


if __name__ == "__main__":
    main()
