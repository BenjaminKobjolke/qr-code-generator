from PIL import Image

from app.core.canvas_composer import CanvasComposer
from app.core.qr_options import BackgroundColor

WHITE = BackgroundColor(255, 255, 255, 255)
BLACK = BackgroundColor(0, 0, 0, 255)
TRANSPARENT = BackgroundColor(0, 0, 0, 0)
RED = BackgroundColor(255, 0, 0, 255)


def test_compose_outputs_exact_dimensions() -> None:
    qr = Image.new("RGB", (50, 50), "black")
    canvas = CanvasComposer().compose(qr, 96, 128, background=WHITE)
    assert canvas.size == (96, 128)


def test_compose_corners_are_white() -> None:
    qr = Image.new("RGB", (40, 40), "black")
    canvas = CanvasComposer().compose(qr, 96, 128, background=WHITE)
    assert canvas.getpixel((0, 0)) == (255, 255, 255)
    assert canvas.getpixel((95, 0)) == (255, 255, 255)
    assert canvas.getpixel((0, 127)) == (255, 255, 255)
    assert canvas.getpixel((95, 127)) == (255, 255, 255)


def test_compose_centers_qr() -> None:
    qr = Image.new("RGB", (40, 40), "black")
    canvas = CanvasComposer().compose(qr, 96, 128, background=WHITE)
    cx, cy = 96 // 2, 128 // 2
    assert canvas.getpixel((cx, cy)) == (0, 0, 0)


def test_compose_qr_larger_than_canvas_does_not_crash() -> None:
    qr = Image.new("RGB", (200, 200), "black")
    canvas = CanvasComposer().compose(qr, 96, 96, background=WHITE)
    assert canvas.size == (96, 96)


def test_compose_square_canvas_has_no_vertical_padding() -> None:
    qr = Image.new("RGB", (96, 96), "black")
    canvas = CanvasComposer().compose(qr, 96, 96, background=WHITE)
    assert canvas.size == (96, 96)
    assert canvas.getpixel((48, 48)) == (0, 0, 0)


def test_compose_black_background_makes_corners_black() -> None:
    qr = Image.new("RGB", (40, 40), "white")
    canvas = CanvasComposer().compose(qr, 96, 128, background=BLACK)
    assert canvas.getpixel((0, 0)) == (0, 0, 0)
    assert canvas.getpixel((95, 127)) == (0, 0, 0)


def test_compose_transparent_background_returns_rgba() -> None:
    qr = Image.new("RGBA", (40, 40), (0, 0, 0, 255))
    canvas = CanvasComposer().compose(qr, 96, 128, background=TRANSPARENT)
    assert canvas.mode == "RGBA"
    corner = canvas.getpixel((0, 0))
    assert isinstance(corner, tuple)
    assert corner[3] == 0


def test_compose_red_background_fills_corners() -> None:
    qr = Image.new("RGB", (40, 40), "black")
    canvas = CanvasComposer().compose(qr, 96, 128, background=RED)
    assert canvas.getpixel((0, 0)) == (255, 0, 0)
    assert canvas.getpixel((95, 127)) == (255, 0, 0)


def test_compose_keep_alpha_with_transparent_qr_shows_canvas_color() -> None:
    qr = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    canvas = CanvasComposer().compose(qr, 96, 128, background=RED, keep_alpha=True)
    assert canvas.mode == "RGBA"
    cx, cy = 48, 64
    pixel = canvas.getpixel((cx, cy))
    assert pixel == (255, 0, 0, 255)
