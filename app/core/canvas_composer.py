from PIL import Image

from app.core.qr_options import BackgroundColor


class CanvasComposer:
    def compose(
        self,
        qr_image: Image.Image,
        width: int,
        height: int,
        *,
        background: BackgroundColor,
        keep_alpha: bool = False,
    ) -> Image.Image:
        canvas = Image.new("RGBA", (width, height), background.rgba_tuple)
        qr_w, qr_h = qr_image.size

        if qr_w > width or qr_h > height:
            crop_left = max(0, (qr_w - width) // 2)
            crop_top = max(0, (qr_h - height) // 2)
            qr_image = qr_image.crop(
                (
                    crop_left,
                    crop_top,
                    crop_left + min(qr_w, width),
                    crop_top + min(qr_h, height),
                )
            )
            qr_w, qr_h = qr_image.size

        x = (width - qr_w) // 2
        y = (height - qr_h) // 2
        if qr_image.mode == "RGBA":
            canvas.paste(qr_image, (x, y), qr_image)
        else:
            canvas.paste(qr_image, (x, y))

        if keep_alpha or background.is_transparent:
            return canvas
        return canvas.convert("RGB")
