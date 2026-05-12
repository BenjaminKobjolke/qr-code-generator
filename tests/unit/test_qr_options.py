import dataclasses
from pathlib import Path

import pytest

from app.core.qr_options import QrOptions


def make_options(**overrides: object) -> QrOptions:
    defaults: dict[str, object] = {
        "url": "https://example.com",
        "width": 96,
        "height": 128,
        "margin_modules": 15,
        "output_path": Path("out.png"),
    }
    defaults.update(overrides)
    return QrOptions(**defaults)  # type: ignore[arg-type]


def test_qr_options_holds_values() -> None:
    opts = make_options()
    assert opts.url == "https://example.com"
    assert opts.width == 96
    assert opts.height == 128
    assert opts.margin_modules == 15
    assert opts.output_path == Path("out.png")


def test_qr_options_is_frozen() -> None:
    opts = make_options()
    with pytest.raises(dataclasses.FrozenInstanceError):
        opts.width = 200  # type: ignore[misc]


def test_qr_options_invert_defaults_false() -> None:
    opts = make_options()
    assert opts.invert is False


def test_qr_options_invert_can_be_set() -> None:
    opts = make_options(invert=True)
    assert opts.invert is True
