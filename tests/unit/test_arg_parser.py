from pathlib import Path

import pytest

from app.cli.arg_parser import ArgValidationError, parse_args
from app.core.qr_options import QrOptions

VALID_ARGS = [
    "--url",
    "https://nrl.li/leadmagnete",
    "--width",
    "96",
    "--height",
    "128",
    "--margin",
    "15",
    "--output",
    "out.png",
]


def test_parse_valid_args_returns_qr_options() -> None:
    opts = parse_args(VALID_ARGS)
    assert isinstance(opts, QrOptions)
    assert opts.url == "https://nrl.li/leadmagnete"
    assert opts.width == 96
    assert opts.height == 128
    assert opts.margin_modules == 15
    assert opts.output_path == Path("out.png")
    assert opts.invert is False


def test_invert_flag_sets_option() -> None:
    opts = parse_args([*VALID_ARGS, "--invert"])
    assert opts.invert is True


def test_missing_required_arg_exits() -> None:
    args = VALID_ARGS.copy()
    idx = args.index("--url")
    del args[idx : idx + 2]
    with pytest.raises(SystemExit):
        parse_args(args)


def test_non_int_width_exits() -> None:
    args = VALID_ARGS.copy()
    args[args.index("--width") + 1] = "abc"
    with pytest.raises(SystemExit):
        parse_args(args)


def test_non_png_output_raises() -> None:
    args = VALID_ARGS.copy()
    args[args.index("--output") + 1] = "out.jpg"
    with pytest.raises(ArgValidationError):
        parse_args(args)


def test_negative_margin_raises() -> None:
    args = VALID_ARGS.copy()
    args[args.index("--margin") + 1] = "-1"
    with pytest.raises(ArgValidationError):
        parse_args(args)


def test_zero_width_raises() -> None:
    args = VALID_ARGS.copy()
    args[args.index("--width") + 1] = "0"
    with pytest.raises(ArgValidationError):
        parse_args(args)


def test_empty_url_raises() -> None:
    args = VALID_ARGS.copy()
    args[args.index("--url") + 1] = ""
    with pytest.raises(ArgValidationError):
        parse_args(args)
