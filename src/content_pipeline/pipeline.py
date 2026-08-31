"""Orchestrates a single brief through generation and quality review."""

from __future__ import annotations

from datetime import datetime, timezone

from . import generator, quality
from .models import Brief, ContentPackage


def run(brief: Brief) -> ContentPackage:
    """Generate all channel content for a brief and review each piece."""
    blog = generator.generate_blog(brief)
    instagram = generator.generate_instagram(brief)
    newsletter = generator.generate_newsletter(brief)

    quality_checks = {
        "blog": quality.review("blog", blog, brief),
        "instagram": quality.review("instagram", instagram, brief),
        "newsletter": quality.review(
            "newsletter", f"{newsletter.subject}\n\n{newsletter.body}", brief
        ),
    }

    return ContentPackage(
        brief=brief,
        blog=blog,
        instagram=instagram,
        newsletter=newsletter,
        quality_checks=quality_checks,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
