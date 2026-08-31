"""
Runtime configuration.

Settings are read from environment variables so no secrets ever need to
be hardcoded or committed to the repository.

Environment variables:
    ANTHROPIC_API_KEY   Your Claude API key. If unset, the pipeline
                        automatically falls back to DEMO_MODE.
    CONTENT_MODEL       Model name to use (default: claude-sonnet-4-6).
    
"""

from __future__ import annotations

import os

ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME: str = os.getenv("CONTENT_MODEL", "claude-sonnet-4-6")

# Demo mode runs the pipeline with realistic canned responses instead of
# calling the API. Useful for demos, CI, and running the repo with zero
# setup. It's automatic (no key -> demo mode) but can be forced on.
DEMO_MODE: bool = ANTHROPIC_API_KEY is None or os.getenv("FORCE_DEMO_MODE") == "1"