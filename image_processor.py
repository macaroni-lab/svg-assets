import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from quality_presets import get_preprocessing_config

class ImageProcessor:
    def __init__(self, preset_config):
        self.config = preset_config
        self.preprocessing_config = get_preprocessing_config()
        
    def process_image(self, image, verbose=True):
        if not self.config["preprocessing"]["enabled"]:
            if verbose:
                print("  前処理スキップ")
            return image
            
        if verbose:
            print("  画像前処理開始...")
            
        processed_image = image.copy()
        
        if self.config["preprocessing"].get("noise_reduction", False):
            processed_image = self._apply_noise_reduction(processed_image, verbose)
            
        if self.config["preprocessing"].get("contrast_enhancement", False):
            processed_image = self._apply_contrast_enhancement(processed_image, verbose)
            
        if self.config["preprocessing"].get("sharpening", False):
            processed_image = self._apply_sharpening(processed_image, verbose)
            
        if self.config["preprocessing"].get("edge_enhancement", False):
            processed_image = self._apply_edge_enhancement(processed_image, verbose)
            
        if verbose:
            print("  前処理完了")
            
        return processed_image
    
    def _apply_noise_reduction(self, image, verbose=True):
        if verbose:
            print("    ノイズ除去適用中...")
            
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        bilateral_config = self.preprocessing_config["noise_reduction"]["bilateral_filter"]
        denoised = cv2.bilateralFilter(
            cv_image,
            bilateral_config["d"],
            bilateral_config["sigma_color"],
            bilateral_config["sigma_space"]
        )
        
        rgb_image = cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)
    
    def _apply_contrast_enhancement(self, image, verbose=True):
        if verbose:
            print("    コントラスト強化適用中...")
            
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        clahe_config = self.preprocessing_config["contrast_enhancement"]["clahe"]
        clahe = cv2.createCLAHE(
            clipLimit=clahe_config["clip_limit"],
            tileGridSize=clahe_config["tile_grid_size"]
        )
        
        l_channel = clahe.apply(l_channel)
        
        enhanced = cv2.merge([l_channel, a_channel, b_channel])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        rgb_image = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)
    
    def _apply_sharpening(self, image, verbose=True):
        if verbose:
            print("    シャープ化適用中...")
            
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        kernel = np.array(self.preprocessing_config["sharpening"]["laplacian_kernel"], dtype=np.float32)
        sharpened = cv2.filter2D(cv_image, -1, kernel)
        
        rgb_image = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(np.clip(rgb_image, 0, 255).astype(np.uint8))
        
        return pil_image
    
    def _apply_edge_enhancement(self, image, verbose=True):
        if verbose:
            print("    エッジ強化適用中...")
            
        enhancer = ImageEnhance.Sharpness(image)
        enhanced = enhancer.enhance(1.5)
        
        edge_filter = ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3)
        enhanced = enhanced.filter(edge_filter)
        
        return enhanced
    
    def resize_image(self, image, verbose=True):
        resize_config = self.config["image_resize"]
        
        if not resize_config["enabled"]:
            if verbose:
                print("  リサイズスキップ（無制限モード）")
            return image
            
        max_width = resize_config["max_width"]
        max_height = resize_config["max_height"]
        
        if max_width is None or max_height is None:
            if verbose:
                print("  リサイズスキップ（無制限サイズ）")
            return image
            
        width, height = image.size
        
        if width <= max_width and height <= max_height:
            if verbose:
                print(f"  リサイズ不要 ({width}x{height})")
            return image
        
        if resize_config["maintain_aspect_ratio"]:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
        else:
            new_width = min(width, max_width)
            new_height = min(height, max_height)
        
        if verbose:
            print(f"  リサイズ: {width}x{height} → {new_width}x{new_height}")
            
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def estimate_processing_time(self, image_size):
        width, height = image_size
        pixels = width * height
        
        base_time = pixels / 1000000
        
        if self.config["preprocessing"]["enabled"]:
            if self.config["preprocessing"].get("noise_reduction", False):
                base_time *= 1.5
            if self.config["preprocessing"].get("contrast_enhancement", False):
                base_time *= 1.3
            if self.config["preprocessing"].get("sharpening", False):
                base_time *= 1.2
            if self.config["preprocessing"].get("edge_enhancement", False):
                base_time *= 1.1
                
        return int(base_time * 10)
    
    def analyze_image_quality(self, image):
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        blur_level = "低" if laplacian_var < 100 else "中" if laplacian_var < 500 else "高"
        
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        contrast = hist.std()
        
        contrast_level = "低" if contrast < 50 else "中" if contrast < 100 else "高"
        
        return {
            "sharpness": laplacian_var,
            "blur_level": blur_level,
            "contrast": contrast,
            "contrast_level": contrast_level,
            "size": image.size
        }