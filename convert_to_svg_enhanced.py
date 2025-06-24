import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import vtracer
from rembg import remove
from io import BytesIO

from config import get_config_for_quality, print_current_config
from quality_presets import list_presets
from image_processor import ImageProcessor
from utils import (
    ProcessingTimer, 
    format_time, 
    create_progress_bar, 
    print_processing_summary,
    print_quality_analysis,
    validate_input_directory,
    create_output_directory,
    clean_temp_files,
    compare_file_sizes,
    print_system_info
)

def ensure_directories(config):
    input_dir = config["base_dirs"]["input"]
    output_dir = config["base_dirs"]["output"]
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    knowledge_images_dir = os.path.join(input_dir, "images")
    if os.path.exists(knowledge_images_dir):
        return knowledge_images_dir
    return input_dir

def get_image_files(input_dir, supported_formats):
    image_files = set()
    for format in supported_formats:
        image_files.update(Path(input_dir).rglob(f"*{format}"))
        image_files.update(Path(input_dir).rglob(f"*{format.upper()}"))
    return list(image_files)

def remove_background(image_path, rembg_config, verbose=True):
    if verbose:
        print(f"  背景除去中...")
    
    with open(image_path, "rb") as input_file:
        input_data = input_file.read()
    
    output_data = remove(
        input_data,
        model=rembg_config["model"],
        alpha_matting=rembg_config["alpha_matting"],
        alpha_matting_foreground_threshold=rembg_config["alpha_matting_foreground_threshold"],
        alpha_matting_background_threshold=rembg_config["alpha_matting_background_threshold"],
        alpha_matting_erode_size=rembg_config["alpha_matting_erode_size"],
    )
    
    return Image.open(BytesIO(output_data))

def convert_to_svg(input_path, config, verbose=True):
    if verbose:
        print(f"\n処理中: {os.path.basename(input_path)}")
    
    timer = ProcessingTimer()
    timer.start()
    
    try:
        processor = ImageProcessor(config["preset"])
        
        if config["processing"]["enable_quality_analysis"] and verbose:
            original_image = Image.open(input_path)
            analysis = processor.analyze_image_quality(original_image)
            print_quality_analysis(analysis)
        
        image_with_no_bg = remove_background(input_path, config["rembg"], verbose)
        
        processed_image = processor.process_image(image_with_no_bg, verbose)
        
        resized_image = processor.resize_image(processed_image, verbose)
        
        temp_filename = f"temp_{os.path.splitext(os.path.basename(input_path))[0]}.png"
        temp_path = os.path.join(config["base_dirs"]["output"], temp_filename)
        resized_image.save(temp_path, "PNG")
        
        if verbose:
            print(f"  SVG変換中...")
        
        svg_filename = os.path.splitext(os.path.basename(input_path))[0] + ".svg"
        svg_path = os.path.join(config["base_dirs"]["output"], svg_filename)
        
        if not os.path.exists(temp_path):
            if verbose:
                print(f"  エラー: 一時ファイルが見つかりません: {temp_path}")
            return False
        
        vtracer_config = config["vtracer"]
        vtracer.convert_image_to_svg_py(
            temp_path,
            svg_path,
            colormode=vtracer_config["colormode"],
            hierarchical=vtracer_config["hierarchical"],
            mode=vtracer_config["mode"],
            filter_speckle=vtracer_config["filter_speckle"],
            color_precision=vtracer_config["color_precision"],
            layer_difference=vtracer_config["layer_difference"],
            corner_threshold=vtracer_config["corner_threshold"],
            length_threshold=vtracer_config["length_threshold"],
            max_iterations=vtracer_config["max_iterations"],
            splice_threshold=vtracer_config["splice_threshold"],
            path_precision=vtracer_config.get("path_precision", 8),
        )
        
        if config["processing"]["cleanup_temp_files"] and os.path.exists(temp_path):
            os.remove(temp_path)
        
        timer.stop()
        
        if verbose:
            size_comparison = compare_file_sizes(input_path, svg_path)
            if size_comparison:
                print(f"  完了: {svg_filename}")
                print(f"    ファイルサイズ: {size_comparison['input_size']} → {size_comparison['output_size']}")
                if size_comparison['size_reduction']:
                    print(f"    圧縮率: {size_comparison['compression_ratio']:.1f}%削減")
                else:
                    print(f"    サイズ変化: {abs(size_comparison['compression_ratio']):.1f}%増加")
            else:
                print(f"  完了: {svg_filename}")
            print(f"    処理時間: {timer.elapsed_formatted()}")
        
        return True
        
    except Exception as e:
        timer.stop()
        if verbose:
            print(f"  エラー: {str(e)}")
            print(f"    処理時間: {timer.elapsed_formatted()}")
        return False

def main():
    parser = argparse.ArgumentParser(description="SVGアセット変換ツール（高品質版）")
    parser.add_argument("--quality", "-q", 
                       choices=["draft", "standard", "high", "ultra"],
                       default="standard",
                       help="品質プリセット (デフォルト: standard)")
    parser.add_argument("--list-presets", action="store_true",
                       help="利用可能な品質プリセットを表示")
    parser.add_argument("--show-config", action="store_true",
                       help="現在の設定を表示")
    parser.add_argument("--system-info", action="store_true",
                       help="システム情報を表示")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="詳細な出力を表示")
    
    args = parser.parse_args()
    
    if args.list_presets:
        list_presets()
        return
    
    if args.system_info:
        print_system_info()
        return
        
    config = get_config_for_quality(args.quality)
    
    if args.verbose:
        config["processing"]["verbose"] = True
    
    if args.show_config:
        print_current_config(args.quality)
        return
    
    print("SVGアセット変換ツール（高品質版）")
    print("=" * 50)
    
    print_current_config(args.quality)
    
    input_dir = ensure_directories(config)
    
    valid, message = validate_input_directory(input_dir, config["supported_formats"])
    if not valid:
        print(f"\nエラー: {message}")
        return
    
    print(f"\n{message}")
    
    success, output_message = create_output_directory(config["base_dirs"]["output"])
    if not success:
        print(f"\nエラー: {output_message}")
        return
    
    image_files = get_image_files(input_dir, config["supported_formats"])
    
    print(f"\n変換を開始します...")
    
    total_timer = ProcessingTimer()
    total_timer.start()
    
    success_count = 0
    for i, image_path in enumerate(image_files, 1):
        if config["processing"]["show_progress"]:
            progress = create_progress_bar(i-1, len(image_files))
            print(f"\n進捗: {progress} ({i}/{len(image_files)})")
        
        if convert_to_svg(str(image_path), config, config["processing"]["verbose"]):
            success_count += 1
    
    total_timer.stop()
    
    if config["processing"]["cleanup_temp_files"]:
        clean_temp_files(config["base_dirs"]["output"])
    
    print_processing_summary(
        success_count, 
        len(image_files), 
        total_timer.elapsed(), 
        config["base_dirs"]["output"]
    )

if __name__ == "__main__":
    main()