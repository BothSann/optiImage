import argparse
import sys
from pathlib import Path

from optiimage import config
from optiimage.converter import convert_image


def _build_output_path(input_path: Path, output_dir: Path | None, fmt: str) -> Path:
    stem = input_path.stem
    extension = f".{fmt}" if fmt != "jpeg" else ".jpg"
    directory = output_dir if output_dir else input_path.parent
    return directory / f"{stem}{extension}"


def _process_file(
    input_path: Path, output_dir: Path | None, fmt: str, quality: int
) -> None:
    output_path = _build_output_path(input_path, output_dir, fmt)
    convert_image(input_path, output_path, quality)
    original_kb = input_path.stat().st_size / 1024
    output_kb = output_path.stat().st_size / 1024
    print(
        f"{input_path.name} -> {output_path.name} ({original_kb:.0f} KB -> {output_kb:.0f} KB)"
    )
    input_path.unlink()


def run() -> None:
    parser = argparse.ArgumentParser(
        prog="optiimage",
        description="Convert and compress images (supports HEIC, JPEG, PNG, WebP)",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=str(config.INPUT_DIR),
        help="Image file or folder (default: input/)",
    )
    parser.add_argument(
        "-f",
        "--format",
        default=config.DEFAULT_OUTPUT_FORMAT,
        choices=config.SUPPORTED_OUTPUT_FORMATS,
        help=f"Output format (default: {config.DEFAULT_OUTPUT_FORMAT})",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=config.DEFAULT_QUALITY,
        help=f"Quality 1-95 (default: {config.DEFAULT_QUALITY})",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(config.OUTPUT_DIR),
        help="Output folder (default: output/)",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    output_dir.mkdir(parents=True, exist_ok=True)

    if input_path.is_dir():
        images = [
            f
            for f in input_path.iterdir()
            if f.suffix.lower() in config.SUPPORTED_INPUT_FORMATS
        ]
        if not images:
            print(f"No supported images found in {input_path}")
            sys.exit(1)
        for image in images:
            _process_file(image, output_dir, args.format, args.quality)
    elif input_path.is_file():
        _process_file(input_path, output_dir, args.format, args.quality)
    else:
        print(f"Error: '{args.input}' is not a valid file or folder")
        sys.exit(1)
