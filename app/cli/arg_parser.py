import argparse
import re
from pathlib import Path

from app.config.constants import (
    HEX_COLOR_PATTERN,
    PNG_EXTENSION,
    TRANSPARENT_KEYWORD,
    ErrorMessages,
)
from app.core.qr_options import BLACK, WHITE, BackgroundColor, QrOptions


class ArgValidationError(ValueError):
    pass


def _parse_color(value: str, flag: str) -> BackgroundColor:
    if value.lower() == TRANSPARENT_KEYWORD:
        return BackgroundColor(0, 0, 0, 0)
    if not re.match(HEX_COLOR_PATTERN, value):
        raise ArgValidationError(ErrorMessages.COLOR_INVALID.format(value=value, flag=flag))
    hex_digits = value.lstrip("#")
    r = int(hex_digits[0:2], 16)
    g = int(hex_digits[2:4], 16)
    b = int(hex_digits[4:6], 16)
    return BackgroundColor(r, g, b, 255)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qr-create",
        description="Generate a damage-resistant QR code (ECC level H) on a fixed-size canvas.",
    )
    parser.add_argument("--url", required=True, help="URL or text to encode.")
    parser.add_argument("--width", required=True, type=int, help="Canvas width in pixels.")
    parser.add_argument("--height", required=True, type=int, help="Canvas height in pixels.")
    parser.add_argument(
        "--margin",
        required=True,
        type=int,
        help="QR border in modules (spec minimum is 4).",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output PNG path (must end in .png).",
    )
    parser.add_argument(
        "--background",
        default=None,
        help="Outer canvas color: 'transparent' or hex RRGGBB. Default white.",
    )
    parser.add_argument(
        "--background-qr",
        default=None,
        help="QR back color (margin + module gaps): 'transparent' or hex RRGGBB. Default white.",
    )
    parser.add_argument(
        "--foreground-qr",
        default=None,
        help="QR module (dark cell) color: 'transparent' or hex RRGGBB. Default black.",
    )
    return parser


def parse_args(argv: list[str]) -> QrOptions:
    parser = _build_parser()
    ns = parser.parse_args(argv)

    url = ns.url.strip() if isinstance(ns.url, str) else ""
    if not url:
        raise ArgValidationError(ErrorMessages.URL_EMPTY)
    if ns.width <= 0:
        raise ArgValidationError(ErrorMessages.WIDTH_NOT_POSITIVE)
    if ns.height <= 0:
        raise ArgValidationError(ErrorMessages.HEIGHT_NOT_POSITIVE)
    if ns.margin < 0:
        raise ArgValidationError(ErrorMessages.MARGIN_NEGATIVE)

    output_path: Path = ns.output
    if output_path.suffix.lower() != PNG_EXTENSION:
        raise ArgValidationError(ErrorMessages.OUTPUT_NOT_PNG)

    parent = output_path.parent
    if str(parent) not in ("", ".") and not parent.exists():
        raise ArgValidationError(ErrorMessages.OUTPUT_DIR_MISSING.format(path=str(parent)))

    canvas_background = (
        _parse_color(ns.background, "--background") if ns.background is not None else WHITE
    )
    qr_background = (
        _parse_color(ns.background_qr, "--background-qr") if ns.background_qr is not None else WHITE
    )
    qr_foreground = (
        _parse_color(ns.foreground_qr, "--foreground-qr") if ns.foreground_qr is not None else BLACK
    )

    return QrOptions(
        url=url,
        width=ns.width,
        height=ns.height,
        margin_modules=ns.margin,
        output_path=output_path,
        canvas_background=canvas_background,
        qr_background=qr_background,
        qr_foreground=qr_foreground,
    )
