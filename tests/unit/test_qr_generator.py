from pathlib import Path

import qrcode
from PIL import Image

from app.core.qr_generator import QrGenerator
from app.core.qr_options import BLACK, WHITE, BackgroundColor, QrOptions


def make_opts(
    width: int = 96,
    height: int = 128,
    margin: int = 15,
    qr_background: BackgroundColor = WHITE,
    qr_foreground: BackgroundColor = BLACK,
) -> QrOptions:
    return QrOptions(
        url="https://nrl.li/leadmagnete",
        width=width,
        height=height,
        margin_modules=margin,
        output_path=Path("out.png"),
        qr_background=qr_background,
        qr_foreground=qr_foreground,
    )


def test_generate_returns_square_pil_image() -> None:
    img = QrGenerator().generate(make_opts())
    assert isinstance(img, Image.Image)
    assert img.size[0] == img.size[1]


def test_generate_fills_min_dimension_exactly() -> None:
    opts = make_opts(width=96, height=128)
    img = QrGenerator().generate(opts)
    assert img.size == (min(opts.width, opts.height), min(opts.width, opts.height))


def test_generate_with_zero_margin_fills_min_dimension() -> None:
    opts = make_opts(width=96, height=128, margin=0)
    img = QrGenerator().generate(opts)
    assert img.size == (96, 96)


def test_generate_uses_ecc_level_h() -> None:
    gen = QrGenerator()
    qr = gen.build_qr(make_opts())
    assert qr.error_correction == qrcode.constants.ERROR_CORRECT_H


def test_generate_uses_requested_border() -> None:
    gen = QrGenerator()
    qr = gen.build_qr(make_opts(margin=15))
    assert qr.border == 15


def test_generate_default_corner_is_white() -> None:
    img = QrGenerator().generate(make_opts())
    assert img.getpixel((0, 0)) == (255, 255, 255, 255)


def test_generate_transparent_qr_background_yields_transparent_corner() -> None:
    img = QrGenerator().generate(make_opts(qr_background=BackgroundColor(0, 0, 0, 0)))
    corner = img.getpixel((0, 0))
    assert isinstance(corner, tuple)
    assert corner[3] == 0


def test_generate_red_foreground_renders_red_modules() -> None:
    red = BackgroundColor(255, 0, 0, 255)
    img = QrGenerator().generate(make_opts(qr_foreground=red))
    # finder pattern at top-left has dark cell at center (~module 3,3)
    found_red = any(
        img.getpixel((x, y)) == (255, 0, 0, 255)
        for x in range(img.size[0])
        for y in range(img.size[1])
    )
    assert found_red


def test_generate_encodes_url() -> None:
    opts = make_opts()
    gen = QrGenerator()
    qr = gen.build_qr(opts)
    encoded = "".join(d.data.decode("utf-8", errors="ignore") for d in qr.data_list)
    assert opts.url in encoded
