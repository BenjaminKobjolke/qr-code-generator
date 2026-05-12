import qrcode
from PIL import Image, ImageDraw

from app.config.constants import (
    DEFAULT_BOX_SIZE,
    ECC_LEVEL,
    ErrorMessages,
)
from app.core.qr_options import QrOptions


class QrGenerationError(RuntimeError):
    pass


class QrGenerator:
    def build_qr(self, opts: QrOptions) -> qrcode.QRCode:
        qr = qrcode.QRCode(
            version=None,
            error_correction=ECC_LEVEL,
            box_size=DEFAULT_BOX_SIZE,
            border=opts.margin_modules,
        )
        qr.add_data(opts.url)
        qr.make(fit=True)
        return qr

    def generate(self, opts: QrOptions) -> Image.Image:
        qr = self.build_qr(opts)
        modules_per_side = qr.modules_count + 2 * opts.margin_modules
        min_dim = min(opts.width, opts.height)

        if modules_per_side > min_dim:
            raise QrGenerationError(ErrorMessages.QR_TOO_LARGE.format(min_dim=min_dim))

        box_size = min_dim // modules_per_side
        if box_size < 1:
            raise QrGenerationError(ErrorMessages.QR_TOO_LARGE.format(min_dim=min_dim))

        matrix = qr.get_matrix()
        side = len(matrix) * box_size
        img = Image.new("RGBA", (side, side), opts.qr_background.rgba_tuple)
        draw = ImageDraw.Draw(img)
        fg = opts.qr_foreground.rgba_tuple
        for row_idx, row in enumerate(matrix):
            for col_idx, is_dark in enumerate(row):
                if is_dark:
                    x0 = col_idx * box_size
                    y0 = row_idx * box_size
                    draw.rectangle(
                        (x0, y0, x0 + box_size - 1, y0 + box_size - 1),
                        fill=fg,
                    )

        if img.size != (min_dim, min_dim):
            img = img.resize((min_dim, min_dim), Image.Resampling.NEAREST)
        return img
