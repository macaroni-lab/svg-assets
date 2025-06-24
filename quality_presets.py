QUALITY_PRESETS = {
    "draft": {
        "name": "ドラフト品質",
        "description": "高速処理優先、基本品質",
        "image_resize": {
            "enabled": True,
            "max_width": 512,
            "max_height": 512,
            "maintain_aspect_ratio": True,
        },
        "preprocessing": {
            "enabled": False,
            "noise_reduction": False,
            "sharpening": False,
            "contrast_enhancement": False,
        },
        "rembg": {
            "model": "u2net",
            "alpha_matting": False,
            "alpha_matting_foreground_threshold": 240,
            "alpha_matting_background_threshold": 50,
            "alpha_matting_erode_size": 10,
        },
        "vtracer": {
            "colormode": "color",
            "hierarchical": "stacked",
            "mode": "spline",
            "filter_speckle": 8,
            "color_precision": 4,
            "layer_difference": 32,
            "corner_threshold": 40,
            "length_threshold": 6.0,
            "max_iterations": 5,
            "splice_threshold": 60,
            "path_precision": 6,
        }
    },
    
    "standard": {
        "name": "標準品質",
        "description": "バランスの取れた品質と速度",
        "image_resize": {
            "enabled": True,
            "max_width": 1024,
            "max_height": 1024,
            "maintain_aspect_ratio": True,
        },
        "preprocessing": {
            "enabled": True,
            "noise_reduction": True,
            "sharpening": False,
            "contrast_enhancement": False,
        },
        "rembg": {
            "model": "u2net",
            "alpha_matting": True,
            "alpha_matting_foreground_threshold": 240,
            "alpha_matting_background_threshold": 50,
            "alpha_matting_erode_size": 10,
        },
        "vtracer": {
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
    },
    
    "high": {
        "name": "高品質",
        "description": "品質重視、処理時間やや長",
        "image_resize": {
            "enabled": True,
            "max_width": 2048,
            "max_height": 2048,
            "maintain_aspect_ratio": True,
        },
        "preprocessing": {
            "enabled": True,
            "noise_reduction": True,
            "sharpening": True,
            "contrast_enhancement": True,
        },
        "rembg": {
            "model": "u2net",
            "alpha_matting": True,
            "alpha_matting_foreground_threshold": 270,
            "alpha_matting_background_threshold": 20,
            "alpha_matting_erode_size": 5,
        },
        "vtracer": {
            "colormode": "color",
            "hierarchical": "stacked",
            "mode": "spline",
            "filter_speckle": 2,
            "color_precision": 8,
            "layer_difference": 8,
            "corner_threshold": 80,
            "length_threshold": 3.5,
            "max_iterations": 15,
            "splice_threshold": 30,
            "path_precision": 10,
        }
    },
    
    "ultra": {
        "name": "ウルトラ品質",
        "description": "最高品質、処理時間長",
        "image_resize": {
            "enabled": False,
            "max_width": None,
            "max_height": None,
            "maintain_aspect_ratio": True,
        },
        "preprocessing": {
            "enabled": True,
            "noise_reduction": True,
            "sharpening": True,
            "contrast_enhancement": True,
            "edge_enhancement": True,
        },
        "rembg": {
            "model": "u2netp",
            "alpha_matting": True,
            "alpha_matting_foreground_threshold": 270,
            "alpha_matting_background_threshold": 15,
            "alpha_matting_erode_size": 3,
        },
        "vtracer": {
            "colormode": "color",
            "hierarchical": "stacked",
            "mode": "spline",
            "filter_speckle": 1,
            "color_precision": 10,
            "layer_difference": 4,
            "corner_threshold": 90,
            "length_threshold": 3.0,
            "max_iterations": 20,
            "splice_threshold": 20,
            "path_precision": 12,
        }
    }
}

PREPROCESSING_CONFIGS = {
    "noise_reduction": {
        "bilateral_filter": {
            "d": 9,
            "sigma_color": 75,
            "sigma_space": 75
        },
        "median_blur": {
            "ksize": 3
        }
    },
    "sharpening": {
        "unsharp_mask": {
            "kernel_size": (0, 0),
            "sigma": 1.0,
            "amount": 1.5,
            "threshold": 0
        },
        "laplacian_kernel": [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ]
    },
    "contrast_enhancement": {
        "clahe": {
            "clip_limit": 2.0,
            "tile_grid_size": (8, 8)
        }
    }
}

def get_preset(preset_name="standard"):
    if preset_name not in QUALITY_PRESETS:
        print(f"警告: 不明な品質プリセット '{preset_name}'。標準品質を使用します。")
        preset_name = "standard"
    return QUALITY_PRESETS[preset_name]

def list_presets():
    print("利用可能な品質プリセット:")
    for name, config in QUALITY_PRESETS.items():
        print(f"  {name}: {config['name']} - {config['description']}")

def get_preprocessing_config():
    return PREPROCESSING_CONFIGS