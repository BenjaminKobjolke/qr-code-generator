from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class QrOptions:
    url: str
    width: int
    height: int
    margin_modules: int
    output_path: Path
