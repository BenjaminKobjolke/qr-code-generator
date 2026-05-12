import subprocess
import sys
from pathlib import Path

from PIL import Image


def _run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "app", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_generates_png_with_requested_dimensions(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--url",
            "https://nrl.li/leadmagnete",
            "--width",
            "96",
            "--height",
            "128",
            "--margin",
            "15",
            "--output",
            str(output),
        ]
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert output.exists()

    with Image.open(output) as img:
        assert img.size == (96, 128)
        rgb = img.convert("RGB")
        assert rgb.getpixel((0, 0)) == (255, 255, 255)
        assert rgb.getpixel((95, 127)) == (255, 255, 255)


def test_cli_background_red_keeps_qr_visible(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--url",
            "https://nrl.li/leadmagnete",
            "--width",
            "96",
            "--height",
            "128",
            "--margin",
            "2",
            "--output",
            str(output),
            "--background",
            "FF0000",
        ]
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    with Image.open(output) as img:
        rgb = img.convert("RGB")
        # canvas corner red
        assert rgb.getpixel((0, 0)) == (255, 0, 0)
        # QR margin/back ring still white (no auto-flip)
        # QR placed at y=16, top of QR back ring around y=16
        assert rgb.getpixel((48, 16)) == (255, 255, 255)
        # finder pattern still has black somewhere
        black_found = any(
            rgb.getpixel((x, y)) == (0, 0, 0) for x in range(96) for y in range(16, 112)
        )
        assert black_found


def test_cli_background_red_with_qr_background_transparent(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--url",
            "https://nrl.li/leadmagnete",
            "--width",
            "96",
            "--height",
            "128",
            "--margin",
            "2",
            "--output",
            str(output),
            "--background",
            "FF0000",
            "--background-qr",
            "transparent",
        ]
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    with Image.open(output) as img:
        assert img.mode == "RGBA"
        # outer canvas red
        assert img.getpixel((0, 0)) == (255, 0, 0, 255)
        # QR back ring pixel should now show red (was transparent in QR, canvas red shows through)
        assert img.getpixel((48, 16)) == (255, 0, 0, 255)


def test_cli_foreground_green_renders_green_modules(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--url",
            "https://nrl.li/leadmagnete",
            "--width",
            "96",
            "--height",
            "128",
            "--margin",
            "2",
            "--output",
            str(output),
            "--foreground-qr",
            "00AA00",
        ]
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    with Image.open(output) as img:
        rgb = img.convert("RGB")
        green_found = any(
            rgb.getpixel((x, y)) == (0, 170, 0) for x in range(96) for y in range(16, 112)
        )
        assert green_found


def test_cli_all_transparent_yields_rgba(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--url",
            "https://nrl.li/leadmagnete",
            "--width",
            "96",
            "--height",
            "128",
            "--margin",
            "2",
            "--output",
            str(output),
            "--background",
            "transparent",
            "--background-qr",
            "transparent",
        ]
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    with Image.open(output) as img:
        assert img.mode == "RGBA"
        corner = img.getpixel((0, 0))
        assert isinstance(corner, tuple)
        assert corner[3] == 0


def test_cli_rejects_invalid_background(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--url",
            "https://example.com",
            "--width",
            "96",
            "--height",
            "128",
            "--margin",
            "2",
            "--output",
            str(output),
            "--background",
            "not-a-color",
        ]
    )
    assert result.returncode != 0
    assert not output.exists()


def test_cli_rejects_invalid_foreground_qr(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--url",
            "https://example.com",
            "--width",
            "96",
            "--height",
            "128",
            "--margin",
            "2",
            "--output",
            str(output),
            "--foreground-qr",
            "zzz",
        ]
    )
    assert result.returncode != 0
    assert not output.exists()


def test_cli_rejects_non_png_output(tmp_path: Path) -> None:
    output = tmp_path / "qr.jpg"
    result = _run_cli(
        [
            "--url",
            "https://example.com",
            "--width",
            "96",
            "--height",
            "96",
            "--margin",
            "4",
            "--output",
            str(output),
        ]
    )
    assert result.returncode != 0
    assert not output.exists()


def test_cli_rejects_missing_url(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = _run_cli(
        [
            "--width",
            "96",
            "--height",
            "96",
            "--margin",
            "4",
            "--output",
            str(output),
        ]
    )
    assert result.returncode != 0
    assert not output.exists()
