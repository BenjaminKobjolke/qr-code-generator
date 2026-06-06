import qrcode.constants

ECC_LEVEL = qrcode.constants.ERROR_CORRECT_H

PNG_EXTENSION = ".png"
DEFAULT_BOX_SIZE = 1

COLOR_BLACK = "black"
COLOR_WHITE = "white"

TRANSPARENT_KEYWORD = "transparent"
HEX_COLOR_PATTERN = r"^#?[0-9A-Fa-f]{6}$"

DEFAULT_SCHEME = "https://"
SCHEME_PATTERN = r"^[a-zA-Z][a-zA-Z0-9+.-]*://"
WWW_PREFIX = "www."
NON_ALNUM_PATTERN = r"[^a-z0-9]+"
FILENAME_DATE_FORMAT = "%Y_%m_%d"
SLUG_FALLBACK = "qr"

CONFIG_FILE_NAME = "config.ini"
CONFIG_ENV_VAR = "QR_CONFIG"


class ConfigKeys:
    OUTPUT_SECTION = "output"
    OUTPUT_DIRECTORY = "directory"
    CANVAS_SECTION = "canvas"
    CANVAS_WIDTH = "width"
    CANVAS_HEIGHT = "height"
    CANVAS_MARGIN = "margin"


class ErrorMessages:
    URL_EMPTY = "URL must not be empty."
    WIDTH_NOT_POSITIVE = "Width must be a positive integer."
    HEIGHT_NOT_POSITIVE = "Height must be a positive integer."
    MARGIN_NEGATIVE = "Margin must be zero or greater."
    OUTPUT_NOT_PNG = "Output path must end in '.png'."
    OUTPUT_DIR_MISSING = "Output directory does not exist: {path}"
    QR_TOO_LARGE = (
        "Requested margin and content do not fit within "
        "min(width, height)={min_dim}px. Increase canvas or shorten URL."
    )
    COLOR_INVALID = (
        "Color value '{value}' for {flag} must be 'transparent' or hex RRGGBB "
        "(optionally prefixed with '#')."
    )
    CONFIG_FILE_MISSING = (
        "Config file not found: {path}. Copy 'config.ini.example' to 'config.ini' and edit it."
    )
    CONFIG_KEY_MISSING = "Config file {path} is missing required key [{section}] {key}."
    CONFIG_VALUE_INVALID = "Config value [{section}] {key}='{value}' in {path} is invalid: {reason}"
    OUTPUT_DIR_UNCREATABLE = "Could not create output directory {path}: {reason}"
    URL_ARG_MISSING = "A single URL argument is required, e.g. qr-create-url www.example.com"


class ExitCodes:
    OK = 0
    UNKNOWN = 1
    INVALID_ARGS = 2
    IO_ERROR = 3
