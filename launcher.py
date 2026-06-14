"""
launcher.py - Entry point for the PyInstaller executable (Phase 5)

This script:
1. Starts the Flask server in a background thread
2. Waits until the server is ready
3. Opens the browser automatically
4. Keeps running until the user closes the window
"""

import sys
import os
import time
import threading
import webbrowser

# ── Path fix for PyInstaller ──────────────────────────────────────────────────
# When running as a .exe, PyInstaller extracts files to a temp folder (_MEIPASS).
# We need to tell Flask where to find the templates folder.
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)
# ─────────────────────────────────────────────────────────────────────────────

from app import app

PORT = 5000
URL = f"http://localhost:{PORT}"


def wait_for_server():
    """Poll until Flask is accepting connections, then open the browser."""
    import urllib.request
    for _ in range(20):
        try:
            urllib.request.urlopen(URL)
            webbrowser.open(URL)
            return
        except Exception:
            time.sleep(0.5)


def run_flask():
    """Run Flask in a background thread."""
    app.run(port=PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    print("=" * 48)
    print("  AI Text Humanizer")
    print(f"  Starting server at {URL}")
    print("  Make sure Ollama is running in the background.")
    print("  Close this window to stop the app.")
    print("=" * 48)

    # Start Flask in a daemon thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Open browser once server is ready
    browser_thread = threading.Thread(target=wait_for_server, daemon=True)
    browser_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down. Goodbye.")
        sys.exit(0)
