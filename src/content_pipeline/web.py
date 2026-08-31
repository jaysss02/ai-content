"""A minimal web front end for the content pipeline."""

from __future__ import annotations

from flask import Flask, render_template, request

from . import config, pipeline, storage
from .models import Brief, ContentPackage, QualityCheck

app = Flask(__name__)


def _brief_from_form(form) -> Brief:
    """Build a Brief from the submitted form fields."""
    key_points = [
        line.strip() for line in form.get("key_points", "").splitlines() if line.strip()
    ]
    return Brief(
        topic=form.get("topic", "").strip(),
        key_points=key_points,
        target_audience=form.get("audience", "").strip(),
        tone=form.get("tone", "").strip(),
    )


def _channels(package: ContentPackage) -> list[dict]:
    """Reshape a ContentPackage into per-channel dicts the template can loop over."""

    def entry(name: str, content: str, check: QualityCheck) -> dict:
        return {
            "name": name,
            "content": content,
            "check": check,
            "passed": all((check.tone_ok, check.no_medical_claims, check.cta_present)),
        }

    return [
        entry("Blog", package.blog, package.quality_checks["blog"]),
        entry("Instagram", package.instagram, package.quality_checks["instagram"]),
        entry(
            "Newsletter",
            f"Subject: {package.newsletter.subject}\n\n{package.newsletter.body}",
            package.quality_checks["newsletter"],
        ),
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    """Show the brief form, and on submit, run the pipeline and render the results."""
    channels = None
    saved_path = None
    error = None

    if request.method == "POST":
        brief = _brief_from_form(request.form)

        if not (brief.topic and brief.key_points and brief.target_audience and brief.tone):
            error = "Please fill in every field, including at least one key point."
        else:
            try:
                package = pipeline.run(brief)
            except Exception as exc:  # external API call - surface failures, don't 500
                error = f"Content generation failed: {exc}"
            else:
                saved_path = storage.save(package)
                channels = _channels(package)

    return render_template(
        "index.html",
        channels=channels,
        saved_path=saved_path,
        error=error,
        demo_mode=config.DEMO_MODE,
        form=request.form,
    )


def main() -> None:
    """Run the Flask development server."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
