from content_pipeline.models import Brief, ContentPackage, Newsletter, QualityCheck


def test_brief_as_dict_roundtrips_fields():
    brief = Brief(
        topic="Cold brew",
        key_points=["Smoother taste", "Less acidic"],
        target_audience="coffee enthusiasts",
        tone="playful",
    )
    assert brief.as_dict() == {
        "topic": "Cold brew",
        "key_points": ["Smoother taste", "Less acidic"],
        "target_audience": "coffee enthusiasts",
        "tone": "playful",
    }


def test_content_package_as_dict_nests_quality_checks():
    brief = Brief(topic="T", key_points=["A"], target_audience="X", tone="Y")
    package = ContentPackage(
        brief=brief,
        blog="blog text",
        instagram="ig text",
        newsletter=Newsletter(subject="Subj", body="Body"),
        quality_checks={
            "blog": QualityCheck(
                tone_ok=True, no_medical_claims=True, cta_present=True, notes="ok"
            )
        },
        generated_at="2026-01-01T00:00:00+00:00",
    )

    data = package.as_dict()

    assert data["brief"]["topic"] == "T"
    assert data["newsletter"] == {"subject": "Subj", "body": "Body"}
    assert data["quality_checks"]["blog"]["tone_ok"] is True
    assert data["generated_at"] == "2026-01-01T00:00:00+00:00"
