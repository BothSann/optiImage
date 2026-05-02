from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

SUPPORTED_INPUT_FORMATS = [".heic", ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]

SUPPORTED_OUTPUT_FORMATS = ["jpeg", "png", "webp"]
DEFAULT_OUTPUT_FORMAT = "jpeg"
DEFAULT_QUALITY = 30
MIN_QUALITY = 1
MAX_QUALITY = 95
