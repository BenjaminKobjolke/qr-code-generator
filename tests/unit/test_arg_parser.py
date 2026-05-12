from pathlib import Path

import pytest

from app.cli.arg_parser import ArgValidationError, parse_args
from app.core.qr_options import BLACK, WHITE, BackgroundColor, QrOptions

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


def test_color_defaults_when_omitted() -> None:
    opts = parse_args(VALID_ARGS)
    assert opts.canvas_background == WHITE
    assert opts.qr_background == WHITE
    assert opts.qr_foreground == BLACK


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


@pytest.mark.parametrize(
    ("flag", "attr"),
    [
        ("--background", "canvas_background"),
        ("--background-qr", "qr_background"),
        ("--foreground-qr", "qr_foreground"),
    ],
)
def test_color_flag_transparent(flag: str, attr: str) -> None:
    opts = parse_args([*VALID_ARGS, flag, "transparent"])
    color = getattr(opts, attr)
    assert color.is_transparent


@pytest.mark.parametrize(
    ("flag", "attr"),
    [
        ("--background", "canvas_background"),
        ("--background-qr", "qr_background"),
        ("--foreground-qr", "qr_foreground"),
    ],
)
def test_color_flag_hex_uppercase(flag: str, attr: str) -> None:
    opts = parse_args([*VALID_ARGS, flag, "FF0080"])
    assert getattr(opts, attr) == BackgroundColor(255, 0, 128, 255)


@pytest.mark.parametrize(
    ("flag", "attr"),
    [
        ("--background", "canvas_background"),
        ("--background-qr", "qr_background"),
        ("--foreground-qr", "qr_foreground"),
    ],
)
def test_color_flag_hex_lowercase_with_hash(flag: str, attr: str) -> None:
    opts = parse_args([*VALID_ARGS, flag, "#00ff80"])
    assert getattr(opts, attr) == BackgroundColor(0, 255, 128, 255)


@pytest.mark.parametrize(
    "flag",
    ["--background", "--background-qr", "--foreground-qr"],
)
def test_color_flag_invalid_raises(flag: str) -> None:
    with pytest.raises(ArgValidationError):
        parse_args([*VALID_ARGS, flag, "not-a-color"])


@pytest.mark.parametrize(
    "flag",
    ["--background", "--background-qr", "--foreground-qr"],
)
def test_color_flag_short_hex_raises(flag: str) -> None:
    with pytest.raises(ArgValidationError):
        parse_args([*VALID_ARGS, flag, "12345"])


def test_color_flags_can_combine() -> None:
    opts = parse_args(
        [
            *VALID_ARGS,
            "--background",
            "FF0000",
            "--background-qr",
            "transparent",
            "--foreground-qr",
            "00FF00",
        ]
    )
    assert opts.canvas_background == BackgroundColor(255, 0, 0, 255)
    assert opts.qr_background.is_transparent
    assert opts.qr_foreground == BackgroundColor(0, 255, 0, 255)
