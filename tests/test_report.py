import json

from imageoptimizer.report import ProcessResult, write_report


def test_report_contains_totals_and_savings(tmp_path):
    result = ProcessResult("a.png", "a.webp", 1000, 600, "PNG", "WEBP", 100, 50)
    assert result.saved_bytes == 400
    assert result.savings_percent == 40.0
    target = tmp_path / "report.json"
    write_report(target, [result])
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["summary"] == {"processed": 1, "input_bytes": 1000, "output_bytes": 600, "saved_bytes": 400}
    assert data["files"][0]["savings_percent"] == 40.0
