from content_pipeline.models import Brief
from content_pipeline.pipeline import run


def _brief() -> Brief:
    return Brief(
        topic="Standing desks",
        key_points=["Reduces back pain", "Boosts energy"],
        target_audience="remote workers",
        tone="upbeat",
    )


def test_run_produces_all_channels_in_demo_mode():
    package = run(_brief())

    assert package.brief.topic == "Standing desks"
    assert "Standing desks" in package.blog
    assert package.instagram
    assert package.newsletter.subject
    assert package.newsletter.body
    assert package.generated_at


def test_run_produces_a_quality_check_per_channel():
    package = run(_brief())

    assert set(package.quality_checks) == {"blog", "instagram", "newsletter"}
    for check in package.quality_checks.values():
        assert check.tone_ok is True
        assert check.no_medical_claims is True
        assert check.cta_present is True
