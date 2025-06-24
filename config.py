import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "knowledge")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".webp", ".bmp"]

VTRACER_CONFIG = {
    "colormode": "color",
    "hierarchical": "stacked",
    "mode": "spline",
    "filter_speckle": 4,
    "color_precision": 6,
    "layer_difference": 16,
    "corner_threshold": 60,
    "length_threshold": 4.0,
    "max_iterations": 10,
    "splice_threshold": 45,
}

IMAGE_RESIZE_CONFIG = {
    "enabled": True,
    "max_width": 1024,
    "max_height": 1024,
    "maintain_aspect_ratio": True,
}

REMBG_CONFIG = {
    "model": "u2net",
    "alpha_matting": True,
    "alpha_matting_foreground_threshold": 240,
    "alpha_matting_background_threshold": 50,
    "alpha_matting_erode_size": 10,
}