from multiprocessing import Value
from pathlib import Path

from PIL import Image
import pillow_heif

from optiimage import config

pillow_heif.register_heif_opener()


def convert_image(input_path: Path, output_path: Path, quality: int) -> None:
    if input_path.suffix.lower() not in config.SUPPORTED_INPUT_FORMATS:
        raise ValueError(f"Unsupported input format: {input_path.suffix}")
    if quality < config.MIN_QUALITY or quality > config.MAX_QUALITY:
        raise ValueError(
            f"Quality must be between {config.MIN_QUALITY} and {config.MAX_QUALITY}"
        )
    with Image.open(input_path) as img:
        rgb = img.convert("RGB")
        rgb.save(output_path, quality=quality, optimize=True)
