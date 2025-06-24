import os
from quality_presets import get_preset, list_presets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "knowledge")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".webp", ".bmp"]

DEFAULT_QUALITY_PRESET = "standard"

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
    "path_precision": 8,
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

PROCESSING_CONFIG = {
    "verbose": True,
    "show_progress": True,
    "enable_quality_analysis": True,
    "cleanup_temp_files": True,
    "max_concurrent_processes": 1,
}

def get_config_for_quality(quality_preset=None):
    if quality_preset is None:
        quality_preset = DEFAULT_QUALITY_PRESET
    
    preset = get_preset(quality_preset)
    
    return {
        "quality_preset": quality_preset,
        "preset": preset,
        "image_resize": preset["image_resize"],
        "rembg": preset["rembg"],
        "vtracer": preset["vtracer"],
        "preprocessing": preset["preprocessing"],
        "base_dirs": {
            "input": INPUT_DIR,
            "output": OUTPUT_DIR,
            "base": BASE_DIR
        },
        "supported_formats": SUPPORTED_FORMATS,
        "processing": PROCESSING_CONFIG
    }

def print_current_config(quality_preset=None):
    config = get_config_for_quality(quality_preset)
    preset = config["preset"]
    
    print(f"\n現在の設定:")
    print(f"  品質プリセット: {config['quality_preset']} - {preset['name']}")
    print(f"  説明: {preset['description']}")
    print(f"  画像リサイズ: {'有効' if preset['image_resize']['enabled'] else '無効'}")
    
    if preset['image_resize']['enabled']:
        max_w = preset['image_resize']['max_width']
        max_h = preset['image_resize']['max_height']
        if max_w and max_h:
            print(f"    最大サイズ: {max_w}x{max_h}")
        else:
            print(f"    最大サイズ: 無制限")
    
    print(f"  前処理: {'有効' if preset['preprocessing']['enabled'] else '無効'}")
    if preset['preprocessing']['enabled']:
        features = []
        if preset['preprocessing'].get('noise_reduction', False):
            features.append("ノイズ除去")
        if preset['preprocessing'].get('sharpening', False):
            features.append("シャープ化")
        if preset['preprocessing'].get('contrast_enhancement', False):
            features.append("コントラスト強化")
        if preset['preprocessing'].get('edge_enhancement', False):
            features.append("エッジ強化")
        if features:
            print(f"    機能: {', '.join(features)}")
    
    print(f"  背景除去モデル: {preset['rembg']['model']}")
    print(f"  アルファマッティング: {'有効' if preset['rembg']['alpha_matting'] else '無効'}")
    print(f"  VTracer色精度: {preset['vtracer']['color_precision']}")
    print(f"  VTracerフィルタスペックル: {preset['vtracer']['filter_speckle']}")

def get_legacy_config():
    return {
        "vtracer": VTRACER_CONFIG,
        "image_resize": IMAGE_RESIZE_CONFIG,
        "rembg": REMBG_CONFIG,
        "input_dir": INPUT_DIR,
        "output_dir": OUTPUT_DIR,
        "supported_formats": SUPPORTED_FORMATS
    }