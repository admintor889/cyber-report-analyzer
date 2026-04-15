from pathlib import Path

from src.ocr.ocr_pipeline import run_ocr


def test_run_ocr_returns_shape() -> None:
    result = run_ocr(Path("img.png"))
    assert "raw_text" in result
    assert "normalized_text" in result
