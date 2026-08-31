from content_pipeline.models import Brief
from content_pipeline.quality import review


def test_review_passes_in_demo_mode():
    brief = Brief(topic="T", key_points=["A"], target_audience="X", tone="Y")

    check = review("blog", "some generated content", brief)

    assert check.tone_ok is True
    assert check.no_medical_claims is True
    assert check.cta_present is True
    assert check.notes
