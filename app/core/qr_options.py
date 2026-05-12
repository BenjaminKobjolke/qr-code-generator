from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class BackgroundColor:
    r: int
    g: int
    b: int
    a: int = 255

    @property
    def is_transparent(self) -> bool:
        return self.a == 0

    @property
    def rgb_tuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @property
    def rgba_tuple(self) -> tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)


WHITE = BackgroundColor(255, 255, 255, 255)
BLACK = BackgroundColor(0, 0, 0, 255)


@dataclass(frozen=True)
class QrOptions:
    url: str
    width: int
    height: int
    margin_modules: int
    output_path: Path
    canvas_background: BackgroundColor = field(default_factory=lambda: WHITE)
    qr_background: BackgroundColor = field(default_factory=lambda: WHITE)
    qr_foreground: BackgroundColor = field(default_factory=lambda: BLACK)

    @property
    def needs_alpha(self) -> bool:
        return (
            self.canvas_background.is_transparent
            or self.qr_background.is_transparent
            or self.qr_foreground.is_transparent
        )
