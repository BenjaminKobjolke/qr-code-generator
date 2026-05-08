# QR Code Generator

CLI tool that generates damage-resistant QR codes (ECC level **H**, ~30% recovery) and
centers them on a fixed-size PNG canvas.

## Requirements

- Python `>=3.11,<3.14`
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

```bat
install.bat
```

This creates the venv via `uv sync --all-extras` and runs the unit tests.

## Usage

```bat
qr-create.bat --url <URL> --width <px> --height <px> --margin <modules> --output <path.png>
```

Example:

```bat
qr-create.bat --url https://nrl.li/leadmagnete --width 96 --height 128 --margin 15 --output sample.png
```

### Arguments

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--url` | string | yes | Text/URL to encode |
| `--width` | int (px) | yes | Final canvas width |
| `--height` | int (px) | yes | Final canvas height |
| `--margin` | int (modules) | yes | QR border in modules (spec minimum is 4) |
| `--output` | path | yes | Output path; must end in `.png` |

### Behavior

- Error correction is hardcoded to level **H** (maximum damage resistance, ~30% recovery).
- The QR is rendered as a square sized to fit `min(width, height)`, then centered on a
  white `width x height` canvas.

## Development

```bat
tools\run_tests.bat                  REM unit tests
tools\run_integration_tests.bat      REM integration tests (CLI end-to-end)
update.bat                           REM upgrade deps + lint + typecheck + tests
```

## Dependencies

- `qrcode[pil] >= 8.0`
- `Pillow >= 11.0`
- Dev: `pytest`, `ruff`, `mypy`
