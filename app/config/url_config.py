import configparser
from dataclasses import dataclass
from pathlib import Path

from app.config.constants import ConfigKeys, ErrorMessages


class UrlConfigError(ValueError):
    pass


@dataclass(frozen=True)
class UrlConfig:
    output_dir: Path
    width: int
    height: int
    margin: int


def _require(parser: configparser.ConfigParser, section: str, key: str, path: Path) -> str:
    if not parser.has_option(section, key):
        raise UrlConfigError(
            ErrorMessages.CONFIG_KEY_MISSING.format(path=path, section=section, key=key)
        )
    return parser.get(section, key).strip()


def _require_int(parser: configparser.ConfigParser, section: str, key: str, path: Path) -> int:
    value = _require(parser, section, key, path)
    try:
        return int(value)
    except ValueError as exc:
        raise UrlConfigError(
            ErrorMessages.CONFIG_VALUE_INVALID.format(
                section=section, key=key, value=value, path=path, reason="must be an integer"
            )
        ) from exc


def load_url_config(path: Path) -> UrlConfig:
    if not path.exists():
        raise UrlConfigError(ErrorMessages.CONFIG_FILE_MISSING.format(path=path))

    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")

    directory = _require(parser, ConfigKeys.OUTPUT_SECTION, ConfigKeys.OUTPUT_DIRECTORY, path)
    if not directory:
        raise UrlConfigError(
            ErrorMessages.CONFIG_VALUE_INVALID.format(
                section=ConfigKeys.OUTPUT_SECTION,
                key=ConfigKeys.OUTPUT_DIRECTORY,
                value=directory,
                path=path,
                reason="must not be empty",
            )
        )

    return UrlConfig(
        output_dir=Path(directory),
        width=_require_int(parser, ConfigKeys.CANVAS_SECTION, ConfigKeys.CANVAS_WIDTH, path),
        height=_require_int(parser, ConfigKeys.CANVAS_SECTION, ConfigKeys.CANVAS_HEIGHT, path),
        margin=_require_int(parser, ConfigKeys.CANVAS_SECTION, ConfigKeys.CANVAS_MARGIN, path),
    )
