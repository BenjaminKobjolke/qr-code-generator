import os
import subprocess
import sys
from datetime import date
from pathlib import Path

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _write_config(tmp_path: Path, out_dir: Path) -> Path:
    cfg = tmp_path / "config.ini"
    cfg.write_text(
        f"[output]\ndirectory = {out_dir}\n\n[canvas]\nwidth = 2048\nheight = 2048\nmargin = 2\n",
        encoding="utf-8",
    )
    return cfg


def _run(
    tmp_path: Path, arg: str, config_path: Path | None = None
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=str(PROJECT_ROOT))
    if config_path is not None:
        env["QR_CONFIG"] = str(config_path)
    else:
        env["QR_CONFIG"] = str(tmp_path / "missing.ini")
    return subprocess.run(
        [sys.executable, "-m", "app.url_runner", arg],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_url_runner_writes_dated_png(tmp_path: Path) -> None:
    out_dir = tmp_path / "qr-codes"
    cfg = _write_config(tmp_path, out_dir)

    result = _run(tmp_path, "www.xida.de", cfg)

    assert result.returncode == 0, f"stderr: {result.stderr}"
    expected = out_dir / f"{date.today():%Y_%m_%d}_xida_de.png"
    assert expected.exists()
    with Image.open(expected) as img:
        assert img.size == (2048, 2048)


def test_url_runner_creates_missing_output_dir(tmp_path: Path) -> None:
    out_dir = tmp_path / "nested" / "qr-codes"
    cfg = _write_config(tmp_path, out_dir)

    result = _run(tmp_path, "https://nrl.li/qualifizierteleads", cfg)

    assert result.returncode == 0, f"stderr: {result.stderr}"
    expected = out_dir / f"{date.today():%Y_%m_%d}_nrl_li_qualifizierteleads.png"
    assert expected.exists()


def test_url_runner_missing_config_fails(tmp_path: Path) -> None:
    result = _run(tmp_path, "www.xida.de")
    assert result.returncode != 0
