from datetime import date

import pytest

from app.core.url_naming import build_filename, normalize_url


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("www.xida.de", "https://www.xida.de"),
        ("  www.xida.de  ", "https://www.xida.de"),
        ("xida.de", "https://xida.de"),
        ("https://nrl.li/x", "https://nrl.li/x"),
        ("http://example.com", "http://example.com"),
        ("ftp://host/file", "ftp://host/file"),
    ],
)
def test_normalize_url(raw: str, expected: str) -> None:
    assert normalize_url(raw) == expected


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.xida.de", "2026_06_06_xida_de.png"),
        ("https://nrl.li/qualifizierteleads", "2026_06_06_nrl_li_qualifizierteleads.png"),
        ("https://example.com/", "2026_06_06_example_com.png"),
        ("https://example.com/path?q=1&a=2", "2026_06_06_example_com_path_q_1_a_2.png"),
        ("https://WWW.Example.COM", "2026_06_06_example_com.png"),
    ],
)
def test_build_filename(url: str, expected: str) -> None:
    assert build_filename(url, date(2026, 6, 6)) == expected


def test_build_filename_empty_slug_falls_back() -> None:
    assert build_filename("https://", date(2026, 6, 6)) == "2026_06_06_qr.png"
