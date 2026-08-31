"""Saves a finished ContentPackage to disk as JSON."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .models import ContentPackage

OUTPUTS_DIR = Path(__file__).resolve().parent.parent.parent / "outputs"


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "content"


def save(package: ContentPackage, output_dir: Path = OUTPUTS_DIR) -> Path:
    """Write the package to `<output_dir>/<timestamp>_<topic-slug>.json`."""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{timestamp}_{_slugify(package.brief.topic)}.json"
    path = output_dir / filename

    path.write_text(json.dumps(package.as_dict(), indent=2), encoding="utf-8")
    return path
