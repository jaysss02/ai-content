"""Command-line entry point.

    python -m content_pipeline --topic "..." --audience "..." --tone "..." \\
        --key-point "..." --key-point "..."

Omit the flags to be prompted for each field interactively instead.
"""

from __future__ import annotations

import argparse
import sys
from . import config, pipeline, storage
from .models import Brief


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="content-pipeline",
        description="Turn a content brief into blog, Instagram, and newsletter copy.",
    )
    parser.add_argument("--topic", help="What the content is about")
    parser.add_argument(
        "--key-point",
        action="append",
        dest="key_points",
        metavar="POINT",
        help="A point the content should cover (repeatable)",
    )
    parser.add_argument("--audience", help="Who the content is for")
    parser.add_argument("--tone", help="Tone of voice, e.g. 'friendly and direct'")
    return parser.parse_args(argv)


def _prompt(label: str) -> str:
    value = input(f"{label}: ").strip()
    while not value:
        value = input(f"{label} (required): ").strip()
    return value


def _prompt_key_points() -> list[str]:
    print("Key points (one per line, blank line to finish):")
    points = []
    while True:
        line = input("- ").strip()
        if not line:
            break
        points.append(line)
    while not points:
        print("At least one key point is required.")
        points = _prompt_key_points()
    return points


def _build_brief(args: argparse.Namespace) -> Brief:
    topic = args.topic or _prompt("Topic")
    audience = args.audience or _prompt("Target audience")
    tone = args.tone or _prompt("Tone")
    key_points = args.key_points or _prompt_key_points()
    return Brief(
        topic=topic, key_points=key_points, target_audience=audience, tone=tone
    )


def main(argv: list[str] | None = None) -> int:
    """Build a brief from CLI args (or prompts), run the pipeline, print the results."""
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    brief = _build_brief(args)

    if config.DEMO_MODE:
        print("Running in DEMO MODE (no ANTHROPIC_API_KEY set) - using canned content.\n")

    package = pipeline.run(brief)
    saved_path = storage.save(package)

    print(f"Saved: {saved_path}\n")
    for channel, check in package.quality_checks.items():
        status = "PASS" if all((check.tone_ok, check.no_medical_claims, check.cta_present)) else "REVIEW"
        print(f"[{status}] {channel}: {check.notes}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
