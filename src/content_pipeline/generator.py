"""Generates channel-adapted content from a Brief.

In DEMO_MODE (no API key configured), canned templates from `demo_data`
are used instead of calling the API - see config.py.
"""

from __future__ import annotations

from functools import lru_cache

import anthropic
from pydantic import BaseModel

from . import config, demo_data
from .models import Brief, Newsletter

BLOG_SYSTEM = """You are a marketing content writer. Write a blog post in \
Markdown from the brief you're given. Aim for 400-600 words with a clear \
headline, a short intro, and a closing call to action. Match the requested \
tone exactly. Do not invent statistics, studies, or claims that aren't in \
the brief."""

INSTAGRAM_SYSTEM = """You are a social media copywriter. Write a single \
Instagram caption from the brief you're given: an attention-grabbing first \
line, a few short lines expanding on the key points, a call to action, and \
3-5 relevant hashtags. Keep it under 150 words. Match the requested tone \
exactly. Do not invent statistics, studies, or claims that aren't in the \
brief."""

NEWSLETTER_SYSTEM = """You are an email newsletter writer. Write a subject \
line and a body from the brief you're given. The body should be 150-300 \
words, written for the target audience, and end with a call to action. \
Match the requested tone exactly. Do not invent statistics, studies, or \
claims that aren't in the brief."""


@lru_cache(maxsize=1)
def get_client() -> anthropic.Anthropic:
    """Return a shared Anthropic client, built once and reused."""
    return anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def _brief_prompt(brief: Brief) -> str:
    points = "\n".join(f"- {point}" for point in brief.key_points)
    return (
        f"Topic: {brief.topic}\n"
        f"Target audience: {brief.target_audience}\n"
        f"Tone: {brief.tone}\n"
        f"Key points to cover:\n{points}"
    )


def _generate_text(system: str, brief: Brief, max_tokens: int = 1024) -> str:
    response = get_client().messages.create(
        model=config.MODEL_NAME,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": _brief_prompt(brief)}],
    )
    return next(block.text for block in response.content if block.type == "text").strip()


def generate_blog(brief: Brief) -> str:
    """Generate a Markdown blog post from a brief."""
    if config.DEMO_MODE:
        return demo_data.demo_blog(brief)
    return _generate_text(BLOG_SYSTEM, brief, max_tokens=2048)


def generate_instagram(brief: Brief) -> str:
    """Generate an Instagram caption from a brief."""
    if config.DEMO_MODE:
        return demo_data.demo_instagram(brief)
    return _generate_text(INSTAGRAM_SYSTEM, brief, max_tokens=512)


class _NewsletterOutput(BaseModel):
    subject: str
    body: str


def generate_newsletter(brief: Brief) -> Newsletter:
    """Generate a newsletter subject and body from a brief."""
    if config.DEMO_MODE:
        return demo_data.demo_newsletter(brief)

    response = get_client().messages.parse(
        model=config.MODEL_NAME,
        max_tokens=1024,
        system=NEWSLETTER_SYSTEM,
        messages=[{"role": "user", "content": _brief_prompt(brief)}],
        output_format=_NewsletterOutput,
    )
    parsed = response.parsed_output
    return Newsletter(subject=parsed.subject, body=parsed.body)
