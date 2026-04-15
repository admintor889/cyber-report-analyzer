from src.reporting.report_exporter import export_summary


def test_export_summary_smoke() -> None:
    data = [{"verdict": "PASS"}, {"verdict": "FAIL"}, {"verdict": "UNKNOWN"}]
    summary = export_summary(data)
    assert summary["PASS"] == 1
    assert summary["FAIL"] == 1
    assert summary["REVIEW"] == 1
