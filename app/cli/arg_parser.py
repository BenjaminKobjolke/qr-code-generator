import argparse
from pathlib import Path

from app.config.constants import PNG_EXTENSION, ErrorMessages
from app.core.qr_options import QrOptions


class ArgValidationError(ValueError):
    pass


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
        "--invert",
        action="store_true",
        help="Inverse colors (white QR on black canvas).",
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

    return QrOptions(
        url=url,
        width=ns.width,
        height=ns.height,
        margin_modules=ns.margin,
        output_path=output_path,
        invert=bool(ns.invert),
    )
