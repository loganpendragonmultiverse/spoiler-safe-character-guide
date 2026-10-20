import json

import pytest

from spoiler_safe_character_guide.cli import main
from spoiler_safe_character_guide.core import analyze, render_json, render_markdown
from spoiler_safe_character_guide.preview import render_html


def fixture():
    return {
        "through": 3,
        "characters": [
            {
                "id": "a",
                "name": "A",
                "facts": [
                    {"text": "early", "milestone": 1},
                    {"text": "FUTURE_FACT", "milestone": 3},
                ],
            },
            {"id": "b", "name": "FUTURE_NAME", "introduced_at": 3},
        ],
        "relationships": [{"source": "a", "target": "b", "text": "FUTURE_REL", "milestone": 1}],
    }


def test_cli_override_all_formats_and_source_unchanged(tmp_path, capsys):
    source = tmp_path / "source.json"
    source.write_text(json.dumps(fixture()))
    before = source.read_bytes()
    for format in ["markdown", "json", "html"]:
        assert main([str(source), "--through", "1", "--format", format]) == 0
        output = capsys.readouterr().out
        assert "early" in output and "FUTURE_" not in output
    assert source.read_bytes() == before
    assert main([str(source), "--through", "-1"]) == 2
    assert "non-negative" in capsys.readouterr().err
    source.write_text("[]")
    assert main([str(source), "--through", "1"]) == 2


def test_large_integer_boundaries_export_exactly():
    n = 2**53
    source = {
        "through": n + 1,
        "characters": [
            {
                "name": "EARLY",
                "introduced_at": n,
                "facts": [{"text": "LATE_FACT", "milestone": n + 1}],
                "aliases": [{"name": "LATE_ALIAS", "milestone": n + 1}],
            },
            {"name": "LATE_NAME", "introduced_at": n + 1},
        ],
    }
    report = analyze(source)
    payload = render_html(report).split('type="application/json">', 1)[1].split("</script>", 1)[0]
    preview = json.loads(payload)
    assert preview["through"] == str(n + 1)
    assert preview["characters"][0]["introduced_at"] == str(n)
    assert preview["characters"][0]["facts"][0]["milestone"] == str(n + 1)
    assert preview["characters"][0]["aliases"][0]["milestone"] == str(n + 1)
    source["through"] = n
    for renderer in [render_json, render_markdown, render_html]:
        assert "LATE_" not in renderer(analyze(source))


@pytest.mark.parametrize("group,key", [("facts", "text"), ("aliases", "name")])
def test_blank_authored_content_rejected(group, key):
    with pytest.raises(ValueError, match="blank"):
        analyze({"through": 0, "characters": [{"name": "A", group: [{key: "  ", "milestone": 0}]}]})
