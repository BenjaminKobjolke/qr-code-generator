import subprocess
import sys
from pathlib import Path

from PIL import Image


def test_cli_generates_png_with_requested_dimensions(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "app",
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
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert output.exists()

    with Image.open(output) as img:
        assert img.size == (96, 128)
        rgb = img.convert("RGB")
        assert rgb.getpixel((0, 0)) == (255, 255, 255)
        assert rgb.getpixel((95, 127)) == (255, 255, 255)


def test_cli_rejects_non_png_output(tmp_path: Path) -> None:
    output = tmp_path / "qr.jpg"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "app",
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
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert not output.exists()


def test_cli_rejects_missing_url(tmp_path: Path) -> None:
    output = tmp_path / "qr.png"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "app",
            "--width",
            "96",
            "--height",
            "96",
            "--margin",
            "4",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert not output.exists()
