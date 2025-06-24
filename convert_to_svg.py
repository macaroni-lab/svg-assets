import os
import sys
from pathlib import Path
from PIL import Image
import vtracer
from rembg import remove
from io import BytesIO

from config import get_config_for_quality, get_legacy_config
from image_processor import ImageProcessor
from utils import ProcessingTimer, format_time, compare_file_sizes

def ensure_directories():
    legacy_config = get_legacy_config()
    os.makedirs(legacy_config["input_dir"], exist_ok=True)
    os.makedirs(legacy_config["output_dir"], exist_ok=True)
    
    knowledge_images_dir = os.path.join(legacy_config["input_dir"], "images")
    if os.path.exists(knowledge_images_dir):
        return knowledge_images_dir
    return legacy_config["input_dir"]

def get_image_files(input_dir):
    legacy_config = get_legacy_config()
    image_files = set()
    for format in legacy_config["supported_formats"]:
        image_files.update(Path(input_dir).rglob(f"*{format}"))
        image_files.update(Path(input_dir).rglob(f"*{format.upper()}"))
    return list(image_files)

def remove_background(image_path):
    print(f"  背景除去中...")
    legacy_config = get_legacy_config()
    
    with open(image_path, "rb") as input_file:
        input_data = input_file.read()
    
    output_data = remove(
        input_data,
        model=legacy_config["rembg"]["model"],
        alpha_matting=legacy_config["rembg"]["alpha_matting"],
        alpha_matting_foreground_threshold=legacy_config["rembg"]["alpha_matting_foreground_threshold"],
        alpha_matting_background_threshold=legacy_config["rembg"]["alpha_matting_background_threshold"],
        alpha_matting_erode_size=legacy_config["rembg"]["alpha_matting_erode_size"],
    )
    
    return Image.open(BytesIO(output_data))

def convert_to_svg(input_path, output_path):
    print(f"\n処理中: {os.path.basename(input_path)}")
    
    timer = ProcessingTimer()
    timer.start()
    legacy_config = get_legacy_config()
    
    try:
        image_with_no_bg = remove_background(input_path)
        
        processor = ImageProcessor({"image_resize": legacy_config["image_resize"]})
        resized_image = processor.resize_image(image_with_no_bg)
        
        temp_filename = f"temp_{os.path.splitext(os.path.basename(input_path))[0]}.png"
        temp_path = os.path.join(legacy_config["output_dir"], temp_filename)
        resized_image.save(temp_path, "PNG")
        
        print(f"  SVG変換中...")
        svg_filename = os.path.splitext(os.path.basename(input_path))[0] + ".svg"
        svg_path = os.path.join(legacy_config["output_dir"], svg_filename)
        
        if not os.path.exists(temp_path):
            print(f"  エラー: 一時ファイルが見つかりません: {temp_path}")
            return False
        
        vtracer.convert_image_to_svg_py(
            temp_path,
            svg_path,
            colormode=legacy_config["vtracer"]["colormode"],
            hierarchical=legacy_config["vtracer"]["hierarchical"],
            mode=legacy_config["vtracer"]["mode"],
            filter_speckle=legacy_config["vtracer"]["filter_speckle"],
            color_precision=legacy_config["vtracer"]["color_precision"],
            layer_difference=legacy_config["vtracer"]["layer_difference"],
            corner_threshold=legacy_config["vtracer"]["corner_threshold"],
            length_threshold=legacy_config["vtracer"]["length_threshold"],
            max_iterations=legacy_config["vtracer"]["max_iterations"],
            splice_threshold=legacy_config["vtracer"]["splice_threshold"],
        )
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        timer.stop()
        
        size_comparison = compare_file_sizes(input_path, svg_path)
        if size_comparison:
            print(f"  完了: {svg_filename}")
            print(f"    ファイルサイズ: {size_comparison['input_size']} → {size_comparison['output_size']}")
            print(f"    処理時間: {timer.elapsed_formatted()}")
        else:
            print(f"  完了: {svg_filename} ({timer.elapsed_formatted()})")
        
        return True
        
    except Exception as e:
        timer.stop()
        print(f"  エラー: {str(e)} ({timer.elapsed_formatted()})")
        return False

def main():
    print("SVGアセット変換ツール")
    print("=" * 50)
    print("ヒント: 高品質変換には 'python convert_to_svg_enhanced.py --quality high' を使用してください")
    
    legacy_config = get_legacy_config()
    input_dir = ensure_directories()
    
    image_files = get_image_files(input_dir)
    
    if not image_files:
        print(f"\n画像ファイルが見つかりません。")
        print(f"以下のフォルダに画像を配置してください:")
        print(f"  {input_dir}")
        print(f"\n対応形式: {', '.join(legacy_config['supported_formats'])}")
        return
    
    print(f"\n{len(image_files)}個の画像ファイルを検出しました。")
    
    total_timer = ProcessingTimer()
    total_timer.start()
    
    success_count = 0
    for image_path in image_files:
        if convert_to_svg(str(image_path), legacy_config["output_dir"]):
            success_count += 1
    
    total_timer.stop()
    
    print(f"\n変換完了: {success_count}/{len(image_files)} ファイル")
    print(f"成功率: {(success_count/len(image_files))*100:.1f}%")
    print(f"総処理時間: {total_timer.elapsed_formatted()}")
    print(f"出力先: {legacy_config['output_dir']}")

if __name__ == "__main__":
    main()