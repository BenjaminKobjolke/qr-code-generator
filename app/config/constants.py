import qrcode.constants

ECC_LEVEL = qrcode.constants.ERROR_CORRECT_H

PNG_EXTENSION = ".png"
DEFAULT_BOX_SIZE = 1


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


class ExitCodes:
    OK = 0
    UNKNOWN = 1
    INVALID_ARGS = 2
    IO_ERROR = 3
