from pathlib import Path

import pytest

from app.config.url_config import UrlConfig, UrlConfigError, load_url_config

VALID_INI = """\
[output]
directory = E:\\out\\qr

[canvas]
width = 2048
height = 2048
margin = 2
"""


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_load_valid_config(tmp_path: Path) -> None:
    cfg_path = _write(tmp_path / "config.ini", VALID_INI)
    cfg = load_url_config(cfg_path)
    assert isinstance(cfg, UrlConfig)
    assert cfg.output_dir == Path("E:\\out\\qr")
    assert cfg.width == 2048
    assert cfg.height == 2048
    assert cfg.margin == 2


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(UrlConfigError):
        load_url_config(tmp_path / "nope.ini")


def test_missing_key_raises(tmp_path: Path) -> None:
    cfg_path = _write(
        tmp_path / "config.ini",
        "[output]\ndirectory = x\n\n[canvas]\nwidth = 1\nheight = 1\n",
    )
    with pytest.raises(UrlConfigError):
        load_url_config(cfg_path)


def test_non_int_canvas_raises(tmp_path: Path) -> None:
    cfg_path = _write(
        tmp_path / "config.ini",
        "[output]\ndirectory = x\n\n[canvas]\nwidth = big\nheight = 1\nmargin = 2\n",
    )
    with pytest.raises(UrlConfigError):
        load_url_config(cfg_path)


def test_empty_directory_raises(tmp_path: Path) -> None:
    cfg_path = _write(
        tmp_path / "config.ini",
        "[output]\ndirectory =\n\n[canvas]\nwidth = 1\nheight = 1\nmargin = 2\n",
    )
    with pytest.raises(UrlConfigError):
        load_url_config(cfg_path)
