"""Typed data structures used across the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class Brief:
    """The single input a human provides. Everything else is derived from it."""

    topic: str
    key_points: list[str]
    target_audience: str
    tone: str

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class QualityCheck:
    """Result of the AI review pass for one piece of content."""

    tone_ok: bool
    no_medical_claims: bool
    cta_present: bool
    notes: str

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Newsletter:
    """The two fields a newsletter needs, where other channels need only one string."""

    subject: str
    body: str

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class ContentPackage:
    """Everything produced for one brief, ready to be saved or reviewed."""

    brief: Brief
    blog: str
    instagram: str
    newsletter: Newsletter
    quality_checks: dict[str, QualityCheck] = field(default_factory=dict)
    generated_at: str = ""

    def as_dict(self) -> dict:
        return {
            "brief": self.brief.as_dict(),
            "blog": self.blog,
            "instagram": self.instagram,
            "newsletter": self.newsletter.as_dict(),
            "quality_checks": {k: v.as_dict() for k, v in self.quality_checks.items()},
            "generated_at": self.generated_at,
        }