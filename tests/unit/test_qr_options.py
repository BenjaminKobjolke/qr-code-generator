import dataclasses
from pathlib import Path

import pytest

from app.core.qr_options import BLACK, WHITE, BackgroundColor, QrOptions


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


def test_qr_options_color_defaults() -> None:
    opts = make_options()
    assert opts.canvas_background == WHITE
    assert opts.qr_background == WHITE
    assert opts.qr_foreground == BLACK


def test_background_color_transparent_helper() -> None:
    assert BackgroundColor(0, 0, 0, 0).is_transparent is True
    assert BackgroundColor(0, 0, 0, 255).is_transparent is False


def test_background_color_tuples() -> None:
    c = BackgroundColor(10, 20, 30, 200)
    assert c.rgb_tuple == (10, 20, 30)
    assert c.rgba_tuple == (10, 20, 30, 200)


def test_needs_alpha_false_for_all_opaque() -> None:
    assert make_options().needs_alpha is False


def test_needs_alpha_true_when_canvas_transparent() -> None:
    opts = make_options(canvas_background=BackgroundColor(0, 0, 0, 0))
    assert opts.needs_alpha is True


def test_needs_alpha_true_when_qr_background_transparent() -> None:
    opts = make_options(qr_background=BackgroundColor(0, 0, 0, 0))
    assert opts.needs_alpha is True


def test_needs_alpha_true_when_qr_foreground_transparent() -> None:
    opts = make_options(qr_foreground=BackgroundColor(0, 0, 0, 0))
    assert opts.needs_alpha is True
