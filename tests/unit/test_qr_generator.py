from pathlib import Path

import qrcode
from PIL import Image

from app.core.qr_generator import QrGenerator
from app.core.qr_options import QrOptions


def make_opts(
    width: int = 96, height: int = 128, margin: int = 15, invert: bool = False
) -> QrOptions:
    return QrOptions(
        url="https://nrl.li/leadmagnete",
        width=width,
        height=height,
        margin_modules=margin,
        output_path=Path("out.png"),
        invert=invert,
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


def test_generate_normal_has_white_border_pixel() -> None:
    img = QrGenerator().generate(make_opts(invert=False))
    assert img.getpixel((0, 0)) == (255, 255, 255)


def test_generate_inverted_has_black_border_pixel() -> None:
    img = QrGenerator().generate(make_opts(invert=True))
    assert img.getpixel((0, 0)) == (0, 0, 0)


def test_generate_encodes_url() -> None:
    opts = make_opts()
    gen = QrGenerator()
    qr = gen.build_qr(opts)
    encoded = "".join(d.data.decode("utf-8", errors="ignore") for d in qr.data_list)
    assert opts.url in encoded
