from PIL import Image


class CanvasComposer:
    def compose(
        self, qr_image: Image.Image, width: int, height: int, *, background: str
    ) -> Image.Image:
        canvas = Image.new("RGB", (width, height), background)
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
        canvas.paste(qr_image, (x, y))
        return canvas
