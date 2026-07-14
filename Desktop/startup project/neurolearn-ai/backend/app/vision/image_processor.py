import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import Dict, Tuple, Optional
from app.config import settings
from loguru import logger


class ImageProcessor:
    def __init__(self):
        self.max_image_size = settings.image_max_size
        self._cv2_available = None

    def _ensure_cv2(self):
        """Check if cv2 is available"""
        if self._cv2_available is None:
            try:
                import cv2
                self._cv2_available = True
            except ImportError:
                logger.warning("OpenCV not available, some image processing features will be disabled")
                self._cv2_available = False
        return self._cv2_available

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        try:
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            image = self._enhance_image(image)
            image = self._denoise_image(image)
            
            return image
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            raise

    def _enhance_image(self, image: Image.Image) -> Image.Image:
        try:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.3)
            
            return image
        except Exception as e:
            logger.error(f"Image enhancement failed: {e}")
            return image

    def _denoise_image(self, image: Image.Image) -> Image.Image:
        try:
            if not self._ensure_cv2():
                return image
                
            import cv2
            np_image = np.array(image)
            
            denoised = cv2.fastNlMeansDenoisingColored(np_image, None, 10, 10, 7, 21)
            
            return Image.fromarray(denoised)
        except Exception as e:
            logger.error(f"Image denoising failed: {e}")
            return image

    def detect_edges(self, image: Image.Image) -> np.ndarray:
        try:
            if not self._ensure_cv2():
                raise RuntimeError("OpenCV not available")
                
            import cv2
            np_image = np.array(image)
            gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
            
            edges = cv2.Canny(gray, 100, 200)
            
            return edges
        except Exception as e:
            logger.error(f"Edge detection failed: {e}")
            raise

    def detect_contours(self, image: Image.Image) -> list:
        try:
            if not self._ensure_cv2():
                raise RuntimeError("OpenCV not available")
                
            import cv2
            np_image = np.array(image)
            gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
            
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            return contours
        except Exception as e:
            logger.error(f"Contour detection failed: {e}")
            raise

    def extract_regions(self, image: Image.Image) -> list:
        try:
            contours = self.detect_contours(image)
            
            import cv2
            regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                if w > 50 and h > 50:
                    regions.append({
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "area": w * h,
                    })
            
            regions.sort(key=lambda x: x["area"], reverse=True)
            
            return regions[:10]
        except Exception as e:
            logger.error(f"Region extraction failed: {e}")
            raise

    def detect_text_regions(self, image: Image.Image) -> list:
        try:
            if not self._ensure_cv2():
                raise RuntimeError("OpenCV not available")
                
            import cv2
            np_image = np.array(image)
            gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
            
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            dilated = cv2.dilate(binary, kernel, iterations=2)
            
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            text_regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                if 0.1 < aspect_ratio < 10 and w > 20 and h > 10:
                    text_regions.append({
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "aspect_ratio": aspect_ratio,
                    })
            
            text_regions.sort(key=lambda x: x["y"])
            
            return text_regions
        except Exception as e:
            logger.error(f"Text region detection failed: {e}")
            raise

    def crop_region(self, image: Image.Image, region: Dict) -> Image.Image:
        try:
            x = region["x"]
            y = region["y"]
            w = region["width"]
            h = region["height"]
            
            cropped = image.crop((x, y, x + w, y + h))
            
            return cropped
        except Exception as e:
            logger.error(f"Region cropping failed: {e}")
            raise

    def resize_image(self, image: Image.Image, max_size: Optional[int] = None) -> Image.Image:
        try:
            max_size = max_size or self.max_image_size
            
            if image.size[0] * image.size[1] > max_size:
                ratio = (max_size / (image.size[0] * image.size[1])) ** 0.5
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.LANCZOS)
            
            return image
        except Exception as e:
            logger.error(f"Image resizing failed: {e}")
            raise

    def validate_image(self, image: Image.Image) -> Dict[str, any]:
        try:
            errors = []
            warnings = []
            
            if image.size[0] < 100 or image.size[1] < 100:
                errors.append("Image resolution too low (minimum 100x100)")
            
            if image.size[0] * image.size[1] > self.max_image_size:
                errors.append(f"Image size exceeds maximum ({self.max_image_size} bytes)")
            
            np_image = np.array(image)
            if np_image.std() < 10:
                warnings.append("Image may have low contrast")
            
            if np.mean(np_image) < 20 or np.mean(np_image) > 235:
                warnings.append("Image may have poor lighting")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "resolution": image.size,
                "mode": image.mode,
            }
        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            return {
                "valid": False,
                "errors": [str(e)],
                "warnings": [],
                "resolution": (0, 0),
                "mode": "unknown",
            }


image_processor = ImageProcessor()
