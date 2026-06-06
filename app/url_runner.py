import os
import sys
from datetime import date
from pathlib import Path

from app.config.constants import (
    CONFIG_ENV_VAR,
    CONFIG_FILE_NAME,
    ErrorMessages,
    ExitCodes,
)
from app.config.settings import Settings
from app.config.url_config import UrlConfig, UrlConfigError, load_url_config
from app.core.qr_options import QrOptions
from app.core.url_naming import build_filename, normalize_url
from app.logging_config import configure_logging, get_logger
from app.main import render


def _config_path() -> Path:
    """Resolve config.ini independent of the current working directory.

    Honors the QR_CONFIG env override, else uses <project_root>/config.ini
    (this file lives at <project_root>/app/url_runner.py).
    """
    override = os.environ.get(CONFIG_ENV_VAR)
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[1] / CONFIG_FILE_NAME


def _build_options(raw_url: str, config: UrlConfig, today: date) -> QrOptions:
    url = normalize_url(raw_url)
    filename = build_filename(url, today)
    return QrOptions(
        url=url,
        width=config.width,
        height=config.height,
        margin_modules=config.margin,
        output_path=config.output_dir / filename,
    )


def run(argv: list[str]) -> int:
    settings = Settings.from_env()
    configure_logging(debug=settings.debug)
    logger = get_logger("qr-create-url")

    if len(argv) != 1 or not argv[0].strip():
        logger.error("%s", ErrorMessages.URL_ARG_MISSING)
        return ExitCodes.INVALID_ARGS

    try:
        config = load_url_config(_config_path())
    except UrlConfigError as exc:
        logger.error("%s", exc)
        return ExitCodes.INVALID_ARGS

    try:
        config.output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.error(
            "%s",
            ErrorMessages.OUTPUT_DIR_UNCREATABLE.format(path=config.output_dir, reason=exc),
        )
        return ExitCodes.IO_ERROR

    opts = _build_options(argv[0], config, date.today())
    return render(opts)


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
