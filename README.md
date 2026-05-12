# QR Code Generator

CLI tool that generates damage-resistant QR codes (ECC level **H**, ~30% recovery) and
centers them on a fixed-size PNG canvas with full control over colors and transparency.

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

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--url` | string | yes | — | Text/URL to encode |
| `--width` | int (px) | yes | — | Final canvas width |
| `--height` | int (px) | yes | — | Final canvas height |
| `--margin` | int (modules) | yes | — | QR border in modules (spec minimum is 4) |
| `--output` | path | yes | — | Output path; must end in `.png` |
| `--background` | color | no | `FFFFFF` | Outer canvas color (area outside the QR square) |
| `--background-qr` | color | no | `FFFFFF` | QR back color (margin / quiet zone + module gaps) |
| `--foreground-qr` | color | no | `000000` | QR module (dark cell) color |

### Color values

The three color flags each accept the same value format:

- `transparent` (case-insensitive) — fully transparent (alpha = 0)
- 6-digit hex RGB, optional leading `#`, case-insensitive — `FF0000`, `#ff0000`, `00aA80`

Invalid values are rejected at startup with a clear error.

### Output format

- If any of the three colors is `transparent`, the PNG is written as **RGBA**.
- Otherwise the PNG is written as **RGB**.

### Behavior

- Error correction is hardcoded to level **H** (~30% recovery).
- The QR is square. It is sized to fit `min(width, height)` and centered on the
  `width x height` canvas. Extra space on the longer axis is filled with `--background`.
- The three color flags are independent. No auto-contrast / auto-flip logic — pick visible
  colors yourself.

### Examples

Default white canvas, normal black-on-white QR:

```bat
qr-create.bat --url https://example.com --width 96 --height 128 --margin 2 --output qr.png
```

Red canvas border, normal QR (visible against any background):

```bat
qr-create.bat --url https://example.com --width 96 --height 128 --margin 2 --background FF0000 --output qr.png
```

Red canvas with QR quiet zone transparent (red shows through the QR margin too):

```bat
qr-create.bat --url https://example.com --width 96 --height 128 --margin 2 ^
              --background FF0000 --background-qr transparent --output qr.png
```

Green QR modules on white canvas:

```bat
qr-create.bat --url https://example.com --width 96 --height 128 --margin 2 ^
              --foreground-qr 00AA00 --output qr.png
```

Fully transparent background — only the QR modules are drawn (RGBA PNG, suitable for
overlaying on any design):

```bat
qr-create.bat --url https://example.com --width 96 --height 128 --margin 2 ^
              --background transparent --background-qr transparent --output qr.png
```

White QR on black canvas (replaces the old `--invert`):

```bat
qr-create.bat --url https://example.com --width 96 --height 128 --margin 2 ^
              --background 000000 --background-qr 000000 --foreground-qr FFFFFF --output qr.png
```

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
