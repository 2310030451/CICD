from PIL import Image
import numpy as np
from typing import Dict, List, Tuple
from app.config import settings
from loguru import logger


class ImageClassifier:
    def __init__(self):
        self._initialized = False
        self.device = None
        self.model = None
        self.transform = None
        self.class_names = [
            "handwritten_notes",
            "math_equation",
            "flowchart",
            "graph",
            "biology_diagram",
            "chemistry_structure",
            "physics_circuit",
            "table",
            "chart",
            "printed_text",
            "whiteboard",
            "screenshot",
        ]

    def _ensure_initialized(self):
        """Lazy initialization to avoid startup errors"""
        if self._initialized:
            return
        
        try:
            import torch
            import torch.nn as nn
            import torchvision.models as models
            from torchvision import transforms
            
            self.device = torch.device("cuda" if torch.cuda.is_available() and settings.enable_gpu else "cpu")
            logger.info(f"Initializing CNN model on {self.device}")
            
            if settings.cnn_model == "efficientnet_b0":
                self.model = models.efficientnet_b0(weights="IMAGENET1K_V1")
                num_features = self.model.classifier[1].in_features
                self.model.classifier = nn.Sequential(
                    nn.Dropout(p=0.2, inplace=True),
                    nn.Linear(num_features, len(self.class_names)),
                )
            elif settings.cnn_model == "resnet50":
                self.model = models.resnet50(weights="IMAGENET1K_V1")
                num_features = self.model.fc.in_features
                self.model.fc = nn.Linear(num_features, len(self.class_names))
            else:
                raise ValueError(f"Unsupported CNN model: {settings.cnn_model}")
            
            self.model = self.model.to(self.device)
            self.model.eval()
            
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            
            self._initialized = True
            logger.info("CNN model initialized successfully")
        except ImportError as e:
            logger.error(f"PyTorch/torchvision not available: {e}")
            self._initialized = False
        except Exception as e:
            logger.error(f"Failed to initialize CNN model: {e}")
            self._initialized = False

    def preprocess_image(self, image: Image.Image):
        try:
            self._ensure_initialized()
            import torch
            
            if image.mode != "RGB":
                image = image.convert("RGB")
            return self.transform(image).unsqueeze(0).to(self.device)
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            raise

    def classify_image(self, image: Image.Image) -> Dict[str, any]:
        try:
            self._ensure_initialized()
            import torch
            
            if not self._initialized:
                raise RuntimeError("CNN model is not available")
                
            input_tensor = self.preprocess_image(image)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            top_prob, top_class = torch.topk(probabilities, min(3, len(self.class_names)))
            
            predictions = []
            for i in range(len(top_prob)):
                predictions.append({
                    "class": self.class_names[top_class[i]],
                    "confidence": float(top_prob[i]),
                })
            
            return {
                "primary_class": self.class_names[top_class[0]],
                "confidence": float(top_prob[0]),
                "predictions": predictions,
                "device": str(self.device),
            }
        except Exception as e:
            logger.error(f"Image classification failed: {e}")
            raise

    def get_image_quality_score(self, image: Image.Image) -> Dict[str, float]:
        try:
            np_image = np.array(image)
            
            if len(np_image.shape) == 3:
                gray = np.mean(np_image, axis=2)
            else:
                gray = np_image
            
            try:
                import cv2
                blur_score = np.var(cv2.Laplacian(gray))
            except ImportError:
                # Fallback if cv2 not available
                blur_score = np.var(gray)  # Simple variance as fallback
            
            brightness = np.mean(gray)
            brightness_score = 1.0 - min(abs(brightness - 128) / 128, 1.0)
            
            contrast = np.std(gray)
            contrast_score = min(contrast / 64, 1.0)
            
            overall_quality = (blur_score / 100 + brightness_score + contrast_score) / 3
            
            return {
                "blur_score": min(blur_score / 100, 1.0),
                "brightness_score": brightness_score,
                "contrast_score": contrast_score,
                "overall_quality": min(overall_quality, 1.0),
                "is_acceptable": overall_quality >= 0.5,
            }
        except Exception as e:
            logger.error(f"Image quality assessment failed: {e}")
            return {
                "blur_score": 0.0,
                "brightness_score": 0.0,
                "contrast_score": 0.0,
                "overall_quality": 0.0,
                "is_acceptable": False,
            }


cnn_classifier = ImageClassifier()
