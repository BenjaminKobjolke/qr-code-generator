import qrcode
from PIL import Image

from app.config.constants import (
    COLOR_BLACK,
    COLOR_WHITE,
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

        qr.box_size = box_size
        fill = COLOR_WHITE if opts.invert else COLOR_BLACK
        back = COLOR_BLACK if opts.invert else COLOR_WHITE
        img = qr.make_image(fill_color=fill, back_color=back)
        rgb: Image.Image = img.convert("RGB")
        if rgb.size != (min_dim, min_dim):
            rgb = rgb.resize((min_dim, min_dim), Image.Resampling.NEAREST)
        return rgb
