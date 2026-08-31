"""AI review pass: checks one piece of generated content against the brief.

In DEMO_MODE this returns a canned passing result instead of calling the
API - see config.py.
"""

from __future__ import annotations

from pydantic import BaseModel

from . import config
from .generator import get_client
from .models import Brief, QualityCheck

REVIEW_SYSTEM = """You are a marketing content quality reviewer. You'll be \
given a content brief and a piece of content generated from it. Check:

- tone_ok: does the content match the requested tone?
- no_medical_claims: does the content avoid medical, health, or efficacy \
claims that aren't explicitly supported by the brief's key points?
- cta_present: does the content end with (or clearly include) a call to \
action?

Set each field to true only if the check passes. In notes, briefly explain \
any failing check; if everything passes, notes can be a short confirmation."""


class _ReviewOutput(BaseModel):
    tone_ok: bool
    no_medical_claims: bool
    cta_present: bool
    notes: str


def _review_prompt(channel: str, content: str, brief: Brief) -> str:
    return (
        f"Channel: {channel}\n"
        f"Brief topic: {brief.topic}\n"
        f"Target audience: {brief.target_audience}\n"
        f"Requested tone: {brief.tone}\n\n"
        f"Content to review:\n{content}"
    )


def _demo_review() -> QualityCheck:
    return QualityCheck(
        tone_ok=True,
        no_medical_claims=True,
        cta_present=True,
        notes="DEMO MODE - quality check not run against the API.",
    )


def review(channel: str, content: str, brief: Brief) -> QualityCheck:
    """Check one piece of generated content against the brief."""
    if config.DEMO_MODE:
        return _demo_review()

    response = get_client().messages.parse(
        model=config.MODEL_NAME,
        max_tokens=512,
        system=REVIEW_SYSTEM,
        messages=[{"role": "user", "content": _review_prompt(channel, content, brief)}],
        output_format=_ReviewOutput,
    )
    parsed = response.parsed_output
    return QualityCheck(
        tone_ok=parsed.tone_ok,
        no_medical_claims=parsed.no_medical_claims,
        cta_present=parsed.cta_present,
        notes=parsed.notes,
    )
