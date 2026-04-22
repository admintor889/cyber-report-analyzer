from __future__ import annotations

import base64
import zlib
from pathlib import Path

import pytest

from src.parser.pdf_parser import extract_text_and_images


ONE_BY_ONE_JPEG_BASE64 = (
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAQEBUQEBAVFRUVFRUVFRUVFRUVFRUVFRUWFhUV"
    "FRUYHSggGBolHRUVITEhJSkrLi4uFx8zODMsNygtLisBCgoKDg0OGxAQGi0lHyUtLS0tLS0tLS0t"
    "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAAEAAgMBIgACEQEDEQH/"
    "xAAbAAABBQEBAAAAAAAAAAAAAAAFAQIDBAYAB//EADQQAAEDAgQDBgUEAwAAAAAAAAEAAgMEEQUS"
    "ITFBBhMiUWFxgZGhFDJCscHR8BVCYnKCorL/xAAaAQEBAQEBAQEAAAAAAAAAAAAAAQIDBAUG/8QAJh"
    "EBAQEAAgICAgMBAAAAAAAAAAECEQMhEjEEQVEiMmEFcYGRof/aAAwDAQACEQMRAD8A9wREQEREBERA"
    "REQEREBERAREQf/Z"
)


def test_extract_text_and_images_requires_path_instance() -> None:
    with pytest.raises(TypeError):
        extract_text_and_images("sample.pdf")  # type: ignore[arg-type]


def test_extract_text_and_images_raises_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        extract_text_and_images(tmp_path / "missing.pdf")


def test_extract_text_and_images_extracts_flate_text_blocks(tmp_path: Path) -> None:
    content_stream = b"BT\n/F1 12 Tf\n72 720 Td\n(Hello S1 MVP) Tj\n(TLS 1.2 Enabled) Tj\nET"
    pdf_bytes = _build_pdf_with_text_stream(zlib.compress(content_stream), flate=True)
    pdf_path = tmp_path / "text-only.pdf"
    pdf_path.write_bytes(pdf_bytes)

    result = extract_text_and_images(pdf_path)

    assert result["image_paths"] == []
    assert result["text_blocks"] == ["Hello S1 MVP\nTLS 1.2 Enabled"]


def test_extract_text_and_images_exports_embedded_jpeg(tmp_path: Path) -> None:
    jpeg_bytes = base64.b64decode(ONE_BY_ONE_JPEG_BASE64)
    pdf_bytes = _build_pdf_with_image_stream(jpeg_bytes)
    pdf_path = tmp_path / "image-only.pdf"
    pdf_path.write_bytes(pdf_bytes)

    result = extract_text_and_images(pdf_path)

    assert result["text_blocks"] == []
    assert len(result["image_paths"]) == 1

    exported_image = Path(result["image_paths"][0])
    assert exported_image.exists()
    assert exported_image.suffix.lower() == ".jpg"
    assert exported_image.read_bytes() == jpeg_bytes


def test_extract_text_and_images_reader_path_extracts_chinese_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pdf_path = tmp_path / "reader.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%%EOF\n")

    class _FakePage:
        def __init__(self, text: str) -> None:
            self._text = text

        def extract_text(self) -> str:
            return self._text

    class _FakeReader:
        def __init__(self, _path: str) -> None:
            self.pages = [_FakePage("第一行中文\n第二行中文"), _FakePage("  第三行中文  ")]

    def _fallback_should_not_run(_pdf_bytes: bytes) -> list[str]:
        raise AssertionError("Fallback parser should not run when reader extraction succeeds")

    monkeypatch.setattr("src.parser.pdf_parser._resolve_pdf_reader", lambda: _FakeReader)
    monkeypatch.setattr("src.parser.pdf_parser._extract_pdf_text_blocks", _fallback_should_not_run)

    result = extract_text_and_images(pdf_path)

    assert result["text_blocks"] == ["第一行中文", "第二行中文", "第三行中文"]


def _build_pdf_with_text_stream(stream_bytes: bytes, *, flate: bool) -> bytes:
    dictionary = f"<< /Length {len(stream_bytes)}".encode("ascii")
    if flate:
        dictionary += b" /Filter /FlateDecode"
    dictionary += b" >>"

    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        + dictionary
        + b"\nstream\n"
        + stream_bytes
        + b"\nendstream\nendobj\n%%EOF\n"
    )


def _build_pdf_with_image_stream(jpeg_bytes: bytes) -> bytes:
    dictionary = (
        b"<< /Type /XObject /Subtype /Image /Width 1 /Height 1 "
        b"/ColorSpace /DeviceRGB /BitsPerComponent 8 "
        b"/Filter /DCTDecode /Length "
        + str(len(jpeg_bytes)).encode("ascii")
        + b" >>"
    )

    return (
        b"%PDF-1.4\n"
        b"2 0 obj\n"
        + dictionary
        + b"\nstream\n"
        + jpeg_bytes
        + b"\nendstream\nendobj\n%%EOF\n"
    )
