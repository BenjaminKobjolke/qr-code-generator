from PIL import Image

from app.core.canvas_composer import CanvasComposer


def test_compose_outputs_exact_dimensions() -> None:
    qr = Image.new("RGB", (50, 50), "black")
    canvas = CanvasComposer().compose(qr, 96, 128)
    assert canvas.size == (96, 128)


def test_compose_corners_are_white() -> None:
    qr = Image.new("RGB", (40, 40), "black")
    canvas = CanvasComposer().compose(qr, 96, 128)
    assert canvas.getpixel((0, 0)) == (255, 255, 255)
    assert canvas.getpixel((95, 0)) == (255, 255, 255)
    assert canvas.getpixel((0, 127)) == (255, 255, 255)
    assert canvas.getpixel((95, 127)) == (255, 255, 255)


def test_compose_centers_qr() -> None:
    qr = Image.new("RGB", (40, 40), "black")
    canvas = CanvasComposer().compose(qr, 96, 128)
    cx, cy = 96 // 2, 128 // 2
    assert canvas.getpixel((cx, cy)) == (0, 0, 0)


def test_compose_qr_larger_than_canvas_does_not_crash() -> None:
    qr = Image.new("RGB", (200, 200), "black")
    canvas = CanvasComposer().compose(qr, 96, 96)
    assert canvas.size == (96, 96)
