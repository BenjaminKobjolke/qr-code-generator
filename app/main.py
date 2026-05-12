from app.cli.arg_parser import ArgValidationError, parse_args
from app.config.constants import ExitCodes
from app.config.settings import Settings
from app.core.canvas_composer import CanvasComposer
from app.core.qr_generator import QrGenerationError, QrGenerator
from app.core.qr_options import BackgroundColor
from app.logging_config import configure_logging, get_logger


def _describe(color: BackgroundColor) -> str:
    if color.is_transparent:
        return "transparent"
    return f"#{color.r:02X}{color.g:02X}{color.b:02X}"


def run(argv: list[str]) -> int:
    settings = Settings.from_env()
    configure_logging(debug=settings.debug)
    logger = get_logger("qr-create")

    try:
        opts = parse_args(argv)
    except ArgValidationError as exc:
        logger.error("Invalid arguments: %s", exc)
        return ExitCodes.INVALID_ARGS
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else ExitCodes.INVALID_ARGS

    try:
        qr_image = QrGenerator().generate(opts)
        canvas = CanvasComposer().compose(
            qr_image,
            opts.width,
            opts.height,
            background=opts.canvas_background,
            keep_alpha=opts.needs_alpha,
        )
        canvas.save(opts.output_path, format="PNG")
    except QrGenerationError as exc:
        logger.error("QR generation failed: %s", exc)
        return ExitCodes.INVALID_ARGS
    except OSError as exc:
        logger.error("I/O error writing %s: %s", opts.output_path, exc)
        return ExitCodes.IO_ERROR
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        return ExitCodes.UNKNOWN

    logger.info(
        "Wrote %s (%dx%d, ECC=H, margin=%d modules, canvas_bg=%s, qr_bg=%s, qr_fg=%s)",
        opts.output_path,
        opts.width,
        opts.height,
        opts.margin_modules,
        _describe(opts.canvas_background),
        _describe(opts.qr_background),
        _describe(opts.qr_foreground),
    )
    return ExitCodes.OK
