from PIL import Image
import numpy as np
from typing import Dict, List, Tuple
from app.config import settings
from loguru import logger


class OCREngine:
    def __init__(self):
        self._initialized = False
        self.ocr = None

    def _ensure_initialized(self):
        """Lazy initialization to avoid startup errors"""
        if self._initialized:
            return
        
        try:
            from paddleocr import PaddleOCR
            
            logger.info(f"Initializing OCR engine: {settings.ocr_engine}")
            
            if settings.ocr_engine == "paddleocr":
                self.ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang="en",
                    use_gpu=settings.enable_gpu,
                    show_log=False,
                )
            else:
                raise ValueError(f"Unsupported OCR engine: {settings.ocr_engine}")
            
            self._initialized = True
            logger.info("OCR engine initialized successfully")
        except ImportError as e:
            logger.error(f"PaddleOCR not available: {e}")
            self._initialized = False
        except Exception as e:
            logger.error(f"Failed to initialize OCR engine: {e}")
            self._initialized = False

    def extract_text(self, image: Image.Image) -> Dict[str, any]:
        try:
            self._ensure_initialized()
            
            if not self._initialized:
                raise RuntimeError("OCR engine is not available")
                
            np_image = np.array(image)
            
            try:
                import cv2
                if len(np_image.shape) == 2:
                    np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2RGB)
                elif np_image.shape[2] == 4:
                    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGBA2RGB)
            except ImportError:
                # Simple fallback without cv2
                if len(np_image.shape) == 2:
                    np_image = np.stack([np_image] * 3, axis=-1)
                elif np_image.shape[2] == 4:
                    np_image = np_image[:, :, :3]
            
            result = self.ocr.ocr(np_image, cls=True)
            
            if not result or not result[0]:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "regions": [],
                    "success": False,
                }
            
            regions = []
            full_text = []
            total_confidence = 0
            region_count = 0
            
            for line in result[0]:
                bbox = line[0]
                text_info = line[1]
                text = text_info[0]
                confidence = text_info[1]
                
                if confidence >= settings.ocr_confidence_threshold:
                    regions.append({
                        "text": text,
                        "confidence": confidence,
                        "bbox": bbox,
                    })
                    full_text.append(text)
                    total_confidence += confidence
                    region_count += 1
            
            avg_confidence = total_confidence / region_count if region_count > 0 else 0.0
            
            return {
                "text": " ".join(full_text),
                "confidence": avg_confidence,
                "regions": regions,
                "success": region_count > 0,
            }
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "regions": [],
                "success": False,
            }

    def extract_handwritten_text(self, image: Image.Image) -> Dict[str, any]:
        try:
            self._ensure_initialized()
            
            if not self._initialized:
                raise RuntimeError("OCR engine is not available")
                
            np_image = np.array(image)
            
            try:
                import cv2
                if len(np_image.shape) == 2:
                    np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2RGB)
                elif np_image.shape[2] == 4:
                    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGBA2RGB)
            except ImportError:
                if len(np_image.shape) == 2:
                    np_image = np.stack([np_image] * 3, axis=-1)
                elif np_image.shape[2] == 4:
                    np_image = np_image[:, :, :3]
            
            result = self.ocr.ocr(np_image, cls=True)
            
            if not result or not result[0]:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "regions": [],
                    "success": False,
                }
            
            regions = []
            full_text = []
            total_confidence = 0
            region_count = 0
            
            for line in result[0]:
                bbox = line[0]
                text_info = line[1]
                text = text_info[0]
                confidence = text_info[1]
                
                regions.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox,
                })
                full_text.append(text)
                total_confidence += confidence
                region_count += 1
            
            avg_confidence = total_confidence / region_count if region_count > 0 else 0.0
            
            return {
                "text": " ".join(full_text),
                "confidence": avg_confidence,
                "regions": regions,
                "success": region_count > 0,
            }
        except Exception as e:
            logger.error(f"Handwritten OCR extraction failed: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "regions": [],
                "success": False,
            }

    def extract_structured_text(self, image: Image.Image) -> Dict[str, any]:
        try:
            self._ensure_initialized()
            
            if not self._initialized:
                raise RuntimeError("OCR engine is not available")
                
            np_image = np.array(image)
            
            try:
                import cv2
                if len(np_image.shape) == 2:
                    np_image = cv2.cvtColor(np_image, cv2.COLOR_GRAY2RGB)
                elif np_image.shape[2] == 4:
                    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGBA2RGB)
            except ImportError:
                if len(np_image.shape) == 2:
                    np_image = np.stack([np_image] * 3, axis=-1)
                elif np_image.shape[2] == 4:
                    np_image = np_image[:, :, :3]
            
            result = self.ocr.ocr(np_image, cls=True)
            
            if not result or not result[0]:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "structured_data": [],
                    "success": False,
                }
            
            lines = result[0]
            structured_data = []
            
            for i, line in enumerate(lines):
                bbox = line[0]
                text_info = line[1]
                text = text_info[0]
                confidence = text_info[1]
                
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                
                structured_data.append({
                    "line_number": i,
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox,
                    "x_min": min(x_coords),
                    "x_max": max(x_coords),
                    "y_min": min(y_coords),
                    "y_max": max(y_coords),
                })
            
            full_text = " ".join([item["text"] for item in structured_data])
            avg_confidence = sum(item["confidence"] for item in structured_data) / len(structured_data)
            
            return {
                "text": full_text,
                "confidence": avg_confidence,
                "structured_data": structured_data,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Structured OCR extraction failed: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "structured_data": [],
                "success": False,
            }


ocr_engine = OCREngine()
