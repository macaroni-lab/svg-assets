import os
import sys
from pathlib import Path
from PIL import Image
import vtracer
from rembg import remove
import config
from io import BytesIO

def ensure_directories():
    os.makedirs(config.INPUT_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    knowledge_images_dir = os.path.join(config.INPUT_DIR, "images")
    if os.path.exists(knowledge_images_dir):
        return knowledge_images_dir
    return config.INPUT_DIR

def get_image_files(input_dir):
    image_files = set()
    for format in config.SUPPORTED_FORMATS:
        image_files.update(Path(input_dir).rglob(f"*{format}"))
        image_files.update(Path(input_dir).rglob(f"*{format.upper()}"))
    return list(image_files)

def resize_image(image, max_width, max_height):
    if not config.IMAGE_RESIZE_CONFIG["enabled"]:
        return image
    
    width, height = image.size
    
    if width <= max_width and height <= max_height:
        return image
    
    if config.IMAGE_RESIZE_CONFIG["maintain_aspect_ratio"]:
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
    else:
        new_width = min(width, max_width)
        new_height = min(height, max_height)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def remove_background(image_path):
    print(f"  背景除去中...")
    
    with open(image_path, "rb") as input_file:
        input_data = input_file.read()
    
    output_data = remove(
        input_data,
        model=config.REMBG_CONFIG["model"],
        alpha_matting=config.REMBG_CONFIG["alpha_matting"],
        alpha_matting_foreground_threshold=config.REMBG_CONFIG["alpha_matting_foreground_threshold"],
        alpha_matting_background_threshold=config.REMBG_CONFIG["alpha_matting_background_threshold"],
        alpha_matting_erode_size=config.REMBG_CONFIG["alpha_matting_erode_size"],
    )
    
    return Image.open(BytesIO(output_data))

def convert_to_svg(input_path, output_path):
    print(f"\n処理中: {os.path.basename(input_path)}")
    
    try:
        image_with_no_bg = remove_background(input_path)
        
        print(f"  リサイズ中...")
        resized_image = resize_image(
            image_with_no_bg,
            config.IMAGE_RESIZE_CONFIG["max_width"],
            config.IMAGE_RESIZE_CONFIG["max_height"]
        )
        
        temp_filename = f"temp_{os.path.splitext(os.path.basename(input_path))[0]}.png"
        temp_path = os.path.join(config.OUTPUT_DIR, temp_filename)
        resized_image.save(temp_path, "PNG")
        
        print(f"  SVG変換中...")
        svg_filename = os.path.splitext(os.path.basename(input_path))[0] + ".svg"
        svg_path = os.path.join(config.OUTPUT_DIR, svg_filename)
        
        if not os.path.exists(temp_path):
            print(f"  エラー: 一時ファイルが見つかりません: {temp_path}")
            return False
            
        print(f"  一時ファイル: {temp_path}")
        print(f"  出力先: {svg_path}")
        
        vtracer.convert_image_to_svg_py(
            temp_path,
            svg_path,
            colormode=config.VTRACER_CONFIG["colormode"],
            hierarchical=config.VTRACER_CONFIG["hierarchical"],
            mode=config.VTRACER_CONFIG["mode"],
            filter_speckle=config.VTRACER_CONFIG["filter_speckle"],
            color_precision=config.VTRACER_CONFIG["color_precision"],
            layer_difference=config.VTRACER_CONFIG["layer_difference"],
            corner_threshold=config.VTRACER_CONFIG["corner_threshold"],
            length_threshold=config.VTRACER_CONFIG["length_threshold"],
            max_iterations=config.VTRACER_CONFIG["max_iterations"],
            splice_threshold=config.VTRACER_CONFIG["splice_threshold"],
        )
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        print(f"  完了: {svg_filename}")
        return True
        
    except Exception as e:
        print(f"  エラー: {str(e)}")
        return False

def main():
    print("SVGアセット変換ツール")
    print("=" * 50)
    
    ensure_directories()
    input_dir = ensure_directories()
    
    image_files = get_image_files(input_dir)
    
    if not image_files:
        print(f"\n画像ファイルが見つかりません。")
        print(f"以下のフォルダに画像を配置してください:")
        print(f"  {input_dir}")
        print(f"\n対応形式: {', '.join(config.SUPPORTED_FORMATS)}")
        return
    
    print(f"\n{len(image_files)}個の画像ファイルを検出しました。")
    
    success_count = 0
    for image_path in image_files:
        if convert_to_svg(str(image_path), config.OUTPUT_DIR):
            success_count += 1
    
    print(f"\n変換完了: {success_count}/{len(image_files)} ファイル")
    print(f"出力先: {config.OUTPUT_DIR}")

if __name__ == "__main__":
    main()