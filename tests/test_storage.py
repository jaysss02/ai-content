import json

from content_pipeline.models import Brief
from content_pipeline.pipeline import run
from content_pipeline.storage import save


def test_save_writes_readable_json(tmp_path):
    brief = Brief(
        topic="Cold Brew Season!",
        key_points=["Smoother taste"],
        target_audience="coffee fans",
        tone="playful",
    )
    package = run(brief)

    path = save(package, output_dir=tmp_path)

    assert path.parent == tmp_path
    assert path.name.endswith("cold-brew-season.json")

    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["brief"]["topic"] == "Cold Brew Season!"
    assert saved["blog"] == package.blog
