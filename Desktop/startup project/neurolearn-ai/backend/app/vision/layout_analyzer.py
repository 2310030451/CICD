import numpy as np
from PIL import Image
from typing import Dict, List, Tuple
from app.config import settings
from loguru import logger


class LayoutAnalyzer:
    def __init__(self):
        self._cv2_available = None

    def _ensure_cv2(self):
        """Check if cv2 is available"""
        if self._cv2_available is None:
            try:
                import cv2
                self._cv2_available = True
            except ImportError:
                logger.warning("OpenCV not available, layout analysis features will be disabled")
                self._cv2_available = False
        return self._cv2_available

    def analyze_layout(self, image: Image.Image) -> Dict[str, any]:
        try:
            if not self._ensure_cv2():
                raise RuntimeError("OpenCV not available for layout analysis")
                
            import cv2
            np_image = np.array(image)
            gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
            
            layout_type = self._detect_layout_type(np_image, gray)
            text_regions = self._detect_text_blocks(gray)
            image_regions = self._detect_image_regions(gray)
            table_regions = self._detect_tables(gray)
            
            return {
                "layout_type": layout_type,
                "text_regions": text_regions,
                "image_regions": image_regions,
                "table_regions": table_regions,
                "has_text": len(text_regions) > 0,
                "has_images": len(image_regions) > 0,
                "has_tables": len(table_regions) > 0,
            }
        except Exception as e:
            logger.error(f"Layout analysis failed: {e}")
            raise

    def _detect_layout_type(self, image: np.ndarray, gray: np.ndarray) -> str:
        try:
            import cv2
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
            
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_count = len(contours)
            
            if edge_density > 0.3 and contour_count > 50:
                return "complex_diagram"
            elif edge_density > 0.15:
                return "structured_document"
            elif contour_count > 20:
                return "mixed_content"
            else:
                return "simple_text"
        except Exception as e:
            logger.error(f"Layout type detection failed: {e}")
            return "unknown"

    def _detect_text_blocks(self, gray: np.ndarray) -> List[Dict]:
        try:
            import cv2
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
            dilated = cv2.dilate(binary, kernel, iterations=1)
            
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            text_blocks = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                if 0.5 < aspect_ratio < 20 and w > 50 and h > 20:
                    text_blocks.append({
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "type": "text_block",
                    })
            
            text_blocks.sort(key=lambda x: x["y"])
            
            return text_blocks
        except Exception as e:
            logger.error(f"Text block detection failed: {e}")
            return []

    def _detect_image_regions(self, gray: np.ndarray) -> List[Dict]:
        try:
            import cv2
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
            dilated = cv2.dilate(binary, kernel, iterations=1)
            
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            image_regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                
                if area > 10000 and w > 100 and h > 100:
                    image_regions.append({
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "area": area,
                        "type": "image_region",
                    })
            
            image_regions.sort(key=lambda x: x["area"], reverse=True)
            
            return image_regions[:5]
        except Exception as e:
            logger.error(f"Image region detection failed: {e}")
            return []

    def _detect_tables(self, gray: np.ndarray) -> List[Dict]:
        try:
            import cv2
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
            
            horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)
            vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
            
            table_mask = cv2.add(horizontal_lines, vertical_lines)
            
            contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            tables = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                
                if area > 5000 and w > 100 and h > 50:
                    tables.append({
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "area": area,
                        "type": "table",
                    })
            
            tables.sort(key=lambda x: x["area"], reverse=True)
            
            return tables[:3]
        except Exception as e:
            logger.error(f"Table detection failed: {e}")
            return []

    def extract_reading_order(self, text_regions: List[Dict]) -> List[Dict]:
        try:
            if not text_regions:
                return []
            
            sorted_regions = sorted(text_regions, key=lambda x: x["y"])
            
            rows = []
            current_row = [sorted_regions[0]]
            current_y = sorted_regions[0]["y"]
            
            for region in sorted_regions[1:]:
                if abs(region["y"] - current_y) < 30:
                    current_row.append(region)
                else:
                    current_row.sort(key=lambda x: x["x"])
                    rows.extend(current_row)
                    current_row = [region]
                    current_y = region["y"]
            
            current_row.sort(key=lambda x: x["x"])
            rows.extend(current_row)
            
            return rows
        except Exception as e:
            logger.error(f"Reading order extraction failed: {e}")
            return text_regions

    def detect_columns(self, text_regions: List[Dict], image_width: int) -> int:
        try:
            if not text_regions:
                return 1
            
            x_positions = [region["x"] for region in text_regions]
            
            if len(x_positions) < 2:
                return 1
            
            x_positions.sort()
            
            gaps = []
            for i in range(1, len(x_positions)):
                gap = x_positions[i] - x_positions[i-1]
                if gap > image_width * 0.1:
                    gaps.append(gap)
            
            if len(gaps) >= 2:
                return min(len(gaps) + 1, 3)
            
            return 1
        except Exception as e:
            logger.error(f"Column detection failed: {e}")
            return 1


layout_analyzer = LayoutAnalyzer()
