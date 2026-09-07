import json

import pytest

from spoiler_safe_character_guide.cli import main
from spoiler_safe_character_guide.core import analyze, render_json, render_markdown
from spoiler_safe_character_guide.preview import render_html


def test_future_names_aliases_facts_and_extension_fields_never_export(tmp_path, capsys) -> None:
    data = {
        "through": 2,
        "characters": [
            {
                "name": "Mara",
                "facts": [
                    {"text": "Ferry owner", "milestone": 1, "secret": "FUTURE_EXTENSION"},
                    {"text": "FUTURE_FACT", "milestone": 3},
                ],
                "aliases": [{"name": "FUTURE_ALIAS", "milestone": 4}],
            },
            {"name": "FUTURE_NAME", "introduced_at": 3},
        ],
    }
    report = analyze(data)
    for render in (render_json, render_markdown, render_html):
        assert "FUTURE_" not in render(report)
        assert "Ferry owner" in render(report)
    source = tmp_path / "input.json"
    source.write_text(json.dumps(data))
    assert main([str(source), "--format", "html"]) == 0
    assert "FUTURE_" not in capsys.readouterr().out


@pytest.mark.parametrize(
    "patch",
    [
        {"characters": {}},
        {"characters": [None]},
        {"through": True},
        {"characters": [{"name": "A", "introduced_at": -1}]},
        {"characters": [{"name": "A", "facts": {}}]},
        {"characters": [{"name": "A", "facts": [None]}]},
        {"characters": [{"name": "A", "facts": [{"text": "A", "milestone": True}]}]},
    ],
)
def test_invalid_nested_fields(patch) -> None:
    with pytest.raises((ValueError, TypeError)):
        analyze({"through": 2, **patch})
