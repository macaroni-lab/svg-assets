import os
import time
from pathlib import Path

def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{int(minutes)}分{remaining_seconds:.0f}秒"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{int(hours)}時間{int(remaining_minutes)}分"

def get_file_info(file_path):
    if not os.path.exists(file_path):
        return None
        
    stat = os.stat(file_path)
    return {
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "modified": time.ctime(stat.st_mtime)
    }

def create_progress_bar(current, total, width=40):
    if total == 0:
        return "[" + "=" * width + "]"
        
    progress = current / total
    filled_width = int(width * progress)
    bar = "=" * filled_width + "-" * (width - filled_width)
    percentage = progress * 100
    
    return f"[{bar}] {percentage:.1f}%"

def print_processing_summary(processed_files, total_files, total_time, output_dir):
    print(f"\n{'='*50}")
    print(f"処理結果サマリー")
    print(f"{'='*50}")
    print(f"処理済みファイル: {processed_files}/{total_files}")
    print(f"成功率: {(processed_files/total_files)*100:.1f}%")
    print(f"総処理時間: {format_time(total_time)}")
    print(f"平均処理時間: {format_time(total_time/total_files if total_files > 0 else 0)}")
    print(f"出力先: {output_dir}")
    
    if processed_files > 0:
        print(f"\n出力ファイル:")
        for svg_file in Path(output_dir).glob("*.svg"):
            info = get_file_info(svg_file)
            if info:
                print(f"  {svg_file.name}: {info['size_formatted']}")

def estimate_total_time(file_count, average_time_per_file):
    total_seconds = file_count * average_time_per_file
    return format_time(total_seconds)

def print_quality_analysis(analysis_results):
    print(f"\n画質分析結果:")
    print(f"  画像サイズ: {analysis_results['size'][0]}x{analysis_results['size'][1]}")
    print(f"  シャープネス: {analysis_results['sharpness']:.2f} ({analysis_results['blur_level']})")
    print(f"  コントラスト: {analysis_results['contrast']:.2f} ({analysis_results['contrast_level']})")

def validate_input_directory(input_dir, supported_formats):
    if not os.path.exists(input_dir):
        return False, f"入力ディレクトリが存在しません: {input_dir}"
    
    if not os.path.isdir(input_dir):
        return False, f"パスがディレクトリではありません: {input_dir}"
    
    image_files = []
    for format in supported_formats:
        image_files.extend(Path(input_dir).rglob(f"*{format}"))
        image_files.extend(Path(input_dir).rglob(f"*{format.upper()}"))
    
    if not image_files:
        return False, f"対応する画像ファイルが見つかりません。対応形式: {', '.join(supported_formats)}"
    
    return True, f"{len(image_files)}個の画像ファイルを検出しました"

def create_output_directory(output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        return True, f"出力ディレクトリを作成しました: {output_dir}"
    except Exception as e:
        return False, f"出力ディレクトリの作成に失敗しました: {str(e)}"

def clean_temp_files(output_dir):
    temp_files = list(Path(output_dir).glob("temp_*"))
    cleaned_count = 0
    
    for temp_file in temp_files:
        try:
            temp_file.unlink()
            cleaned_count += 1
        except Exception as e:
            print(f"警告: 一時ファイルの削除に失敗しました: {temp_file.name} - {str(e)}")
    
    if cleaned_count > 0:
        print(f"一時ファイル{cleaned_count}個を削除しました")

def compare_file_sizes(input_file, output_file):
    input_info = get_file_info(input_file)
    output_info = get_file_info(output_file)
    
    if not input_info or not output_info:
        return None
    
    compression_ratio = (1 - (output_info["size"] / input_info["size"])) * 100
    
    return {
        "input_size": input_info["size_formatted"],
        "output_size": output_info["size_formatted"],
        "compression_ratio": compression_ratio,
        "size_reduction": compression_ratio > 0
    }

class ProcessingTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        
    def start(self):
        self.start_time = time.time()
        
    def stop(self):
        self.end_time = time.time()
        
    def elapsed(self):
        if self.start_time is None:
            return 0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
        
    def elapsed_formatted(self):
        return format_time(self.elapsed())

def print_system_info():
    print("システム情報:")
    print(f"  作業ディレクトリ: {os.getcwd()}")
    print(f"  Pythonパス: {os.path.dirname(os.__file__)}")
    
    try:
        import cv2
        print(f"  OpenCV: {cv2.__version__}")
    except ImportError:
        print("  OpenCV: インストールされていません")
    
    try:
        import vtracer
        print("  VTracer: インストール済み")
    except ImportError:
        print("  VTracer: インストールされていません")
    
    try:
        import rembg
        print("  Rembg: インストール済み")
    except ImportError:
        print("  Rembg: インストールされていません")