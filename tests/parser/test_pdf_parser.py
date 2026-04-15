from pathlib import Path

from src.parser.pdf_parser import extract_text_and_images


def test_extract_text_and_images_returns_shape() -> None:
    result = extract_text_and_images(Path("sample.pdf"))
    assert "text_blocks" in result
    assert "image_paths" in result
