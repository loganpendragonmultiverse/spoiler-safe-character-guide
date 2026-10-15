import copy

import pytest

from spoiler_safe_character_guide.core import analyze, render_json, render_markdown
from spoiler_safe_character_guide.preview import render_html


def data():
    return {
        "through": 2,
        "characters": [
            {"id": "a", "name": "A"},
            {"id": "FUTURE_ID", "name": "FUTURE_NAME", "introduced_at": 3},
        ],
        "relationships": [
            {"source": "a", "target": "FUTURE_ID", "text": "FUTURE_REL", "milestone": 1}
        ],
    }


def test_endpoints_boundary_and_exports():
    source = data()
    before = copy.deepcopy(source)
    for render in (render_json, render_markdown, render_html):
        assert "FUTURE" not in render(analyze(source))
    source["through"] = 3
    report = analyze(source)
    assert report["relationships"][0]["milestone"] == 3
    assert "FUTURE_ID" not in render_json(report)
    assert source["characters"] == before["characters"]


def test_relationship_boundary_and_legacy():
    source = data()
    source["characters"][1]["introduced_at"] = 0
    source["relationships"][0]["milestone"] = 3
    assert not analyze(source)["relationships"]
    source["through"] = 3
    assert len(analyze(source)["relationships"]) == 1
    assert "relationships" not in analyze({"through": 0})


@pytest.mark.parametrize(
    "patch",
    [
        {"relationships": {}},
        {"relationships": [None]},
        {"relationships": [{"source": "missing", "target": "a", "text": "x", "milestone": 0}]},
        {"relationships": [{"source": "a", "target": "a", "text": "", "milestone": 0}]},
        {"relationships": [{"source": "a", "target": "a", "text": "x", "milestone": True}]},
        {"characters": [{"id": "a", "name": "A"}, {"id": "a", "name": "B"}]},
    ],
)
def test_schema(patch):
    with pytest.raises((ValueError, TypeError)):
        analyze({**data(), **patch})
