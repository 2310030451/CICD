from datetime import datetime
from typing import Optional, List
from app.models.vision import VisionImageCreate, VisionImageUpdate, VisionImageInDB, ProcessingStatus
from app.core.database import get_database
from app.vision.cnn_model import cnn_classifier
from app.vision.ocr_engine import ocr_engine
from app.vision.image_processor import image_processor
from app.vision.layout_analyzer import layout_analyzer
from app.ai.rag import rag_pipeline
from app.config import settings
from loguru import logger
import hashlib
import os
from PIL import Image


class VisionService:
    def __init__(self):
        self.db = None

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_vision_image(self, image_data: VisionImageCreate) -> VisionImageInDB:
        db = await self.get_database()
        image_dict = image_data.model_dump()
        image_dict["status"] = ProcessingStatus.PENDING
        image_dict["classification_confidence"] = 0.0
        image_dict["ocr_confidence"] = 0.0
        image_dict["created_at"] = datetime.utcnow()
        image_dict["updated_at"] = datetime.utcnow()
        
        result = await db.vision_images.insert_one(image_dict)
        image_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Vision image created with ID: {result.inserted_id}")
        return VisionImageInDB(**image_dict)

    async def get_vision_image_by_id(self, image_id: str, user_id: str) -> Optional[VisionImageInDB]:
        db = await self.get_database()
        image_doc = await db.vision_images.find_one({"_id": image_id, "user_id": user_id})
        
        if image_doc:
            image_doc["_id"] = str(image_doc["_id"])
            return VisionImageInDB(**image_doc)
        return None

    async def get_user_vision_images(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        status_filter: Optional[ProcessingStatus] = None
    ) -> List[VisionImageInDB]:
        db = await self.get_database()
        query = {"user_id": user_id}
        if status_filter:
            query["status"] = status_filter
        
        cursor = db.vision_images.find(query).sort("created_at", -1).skip(skip).limit(limit)
        images = await cursor.to_list(length=limit)
        
        for image in images:
            image["_id"] = str(image["_id"])
        
        return [VisionImageInDB(**image) for image in images]

    async def update_vision_image(self, image_id: str, image_update: VisionImageUpdate, user_id: str) -> Optional[VisionImageInDB]:
        db = await self.get_database()
        update_data = {k: v for k, v in image_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.vision_images.update_one(
            {"_id": image_id, "user_id": user_id},
            {"": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_vision_image_by_id(image_id, user_id)
        return None

    async def delete_vision_image(self, image_id: str, user_id: str) -> bool:
        db = await self.get_database()
        
        image = await self.get_vision_image_by_id(image_id, user_id)
        if not image:
            return False
        
        file_path = os.path.join(settings.upload_directory, image.file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        result = await db.vision_images.delete_one({"_id": image_id, "user_id": user_id})
        return result.deleted_count > 0

    async def process_vision_image(self, image_id: str):
        try:
            db = await self.get_database()
            image = await db.vision_images.find_one({"_id": image_id})
            
            if not image:
                logger.error(f"Vision image {image_id} not found")
                return
            
            await db.vision_images.update_one(
                {"_id": image_id},
                {"": {"status": ProcessingStatus.PROCESSING}}
            )
            
            file_path = os.path.join(settings.upload_directory, image["file_name"])
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            pil_image = Image.open(file_path)
            
            validation = image_processor.validate_image(pil_image)
            if not validation["valid"]:
                raise ValueError(f"Image validation failed: {validation['errors']}")
            
            pil_image = image_processor.preprocess_image(pil_image)
            
            classification = cnn_classifier.classify_image(pil_image)
            image_quality = cnn_classifier.get_image_quality_score(pil_image)
            
            if not image_quality["is_acceptable"]:
                raise ValueError("Image quality is too low for processing")
            
            ocr_result = ocr_engine.extract_text(pil_image)
            
            layout_result = layout_analyzer.analyze_layout(pil_image)
            
            context_text = f"Image type: {classification['primary_class']}. "
            context_text += f"OCR extracted text: {ocr_result['text']}. "
            context_text += f"Layout: {layout_result['layout_type']}."
            
            explanation = ""
            if ocr_result["text"]:
                try:
                    response = await rag_pipeline.query(
                        question=f"Explain this {classification['primary_class']} with the following content: {ocr_result['text'][:500]}",
                        user_id=image["user_id"],
                    )
                    explanation = response["answer"]
                except Exception as e:
                    logger.warning(f"AI explanation generation failed: {e}")
                    explanation = f"This appears to be a {classification['primary_class'].replace('_', ' ')} with extracted text: {ocr_result['text'][:200]}..."
            
            await db.vision_images.update_one(
                {"_id": image_id},
                {
                    "": {
                        "status": ProcessingStatus.COMPLETED,
                        "image_type": classification["primary_class"],
                        "classification_confidence": classification["confidence"],
                        "ocr_text": ocr_result["text"],
                        "ocr_confidence": ocr_result["confidence"],
                        "layout_analysis": layout_result,
                        "image_quality": image_quality,
                        "ai_explanation": explanation,
                        "processed_at": datetime.utcnow(),
                    }
                }
            )
            
            logger.info(f"Vision image {image_id} processed successfully")
        except Exception as e:
            logger.error(f"Vision image processing failed for {image_id}: {e}")
            await db.vision_images.update_one(
                {"_id": image_id},
                {
                    "": {
                        "status": ProcessingStatus.FAILED,
                        "error_message": str(e),
                    }
                }
            )
            raise

    async def generate_quiz_from_image(self, image_id: str, user_id: str) -> dict:
        try:
            image = await self.get_vision_image_by_id(image_id, user_id)
            if not image:
                raise ValueError("Image not found")
            
            if not image.ocr_text:
                raise ValueError("No OCR text available for quiz generation")
            
            response = await rag_pipeline.query(
                question=f"Generate a quiz with 5 questions based on this content: {image.ocr_text}",
                user_id=user_id,
            )
            
            quiz_data = {
                "title": f"Quiz from {image.title}",
                "questions": response["answer"],
                "generated_at": datetime.utcnow().isoformat(),
            }
            
            await db.vision_images.update_one(
                {"_id": image_id},
                {"": {"generated_quiz": quiz_data}}
            )
            
            return quiz_data
        except Exception as e:
            logger.error(f"Quiz generation failed: {e}")
            raise

    async def generate_flashcards_from_image(self, image_id: str, user_id: str) -> List[dict]:
        try:
            image = await self.get_vision_image_by_id(image_id, user_id)
            if not image:
                raise ValueError("Image not found")
            
            if not image.ocr_text:
                raise ValueError("No OCR text available for flashcard generation")
            
            response = await rag_pipeline.query(
                question=f"Generate 10 flashcards (front/back pairs) from this content: {image.ocr_text}",
                user_id=user_id,
            )
            
            flashcards = []
            lines = response["answer"].split("\n")
            for line in lines:
                if ":" in line:
                    parts = line.split(":", 1)
                    flashcards.append({
                        "front": parts[0].strip(),
                        "back": parts[1].strip(),
                    })
            
            await db.vision_images.update_one(
                {"_id": image_id},
                {"": {"generated_flashcards": flashcards}}
            )
            
            return flashcards
        except Exception as e:
            logger.error(f"Flashcard generation failed: {e}")
            raise
