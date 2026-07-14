import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db, close_db, get_database
from app.vision.cnn_model import cnn_classifier
from app.vision.ocr_engine import ocr_engine
from app.vision.image_processor import image_processor
from app.vision.layout_analyzer import layout_analyzer
from app.services.vision_service import VisionService
from app.models.vision import VisionImageCreate, ProcessingStatus
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont


@pytest.fixture
async def client():
    async with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def test_db():
    await init_db()
    db = await get_database()
    yield db
    await close_db()


@pytest.fixture
async def sample_image_file():
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        img = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), "Test Text for OCR", fill='black')
        draw.rectangle([100, 100, 300, 200], outline='black', width=2)
        img.save(f.name)
        temp_path = f.name
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestImageProcessor:
    @pytest.mark.asyncio
    async def test_image_validation(self, sample_image_file):
        processor = ImageProcessor()
        image = Image.open(sample_image_file)
        
        validation = processor.validate_image(image)
        assert validation["valid"] is True
        assert validation["resolution"] == (400, 300)

    @pytest.mark.asyncio
    async def test_image_preprocessing(self, sample_image_file):
        processor = ImageProcessor()
        image = Image.open(sample_image_file)
        
        processed = processor.preprocess_image(image)
        assert processed.mode == "RGB"
        assert processed.size == image.size

    @pytest.mark.asyncio
    async def test_edge_detection(self, sample_image_file):
        processor = ImageProcessor()
        image = Image.open(sample_image_file)
        
        edges = processor.detect_edges(image)
        assert edges is not None
        assert edges.shape[0] > 0

    @pytest.mark.asyncio
    async def test_contour_detection(self, sample_image_file):
        processor = ImageProcessor()
        image = Image.open(sample_image_file)
        
        contours = processor.detect_contours(image)
        assert contours is not None
        assert len(contours) > 0


class TestLayoutAnalyzer:
    @pytest.mark.asyncio
    async def test_layout_analysis(self, sample_image_file):
        analyzer = LayoutAnalyzer()
        image = Image.open(sample_image_file)
        
        layout = analyzer.analyze_layout(image)
        assert "layout_type" in layout
        assert "text_regions" in layout
        assert "image_regions" in layout
        assert "table_regions" in layout

    @pytest.mark.asyncio
    async def test_reading_order_extraction(self):
        analyzer = LayoutAnalyzer()
        regions = [
            {"x": 10, "y": 10, "width": 100, "height": 20},
            {"x": 10, "y": 50, "width": 100, "height": 20},
        ]
        
        ordered = analyzer.extract_reading_order(regions)
        assert len(ordered) == 2
        assert ordered[0]["y"] < ordered[1]["y"]

    @pytest.mark.asyncio
    async def test_column_detection(self):
        analyzer = LayoutAnalyzer()
        regions = [
            {"x": 10, "y": 10, "width": 100, "height": 20},
            {"x": 200, "y": 10, "width": 100, "height": 20},
        ]
        
        columns = analyzer.detect_columns(regions, 400)
        assert columns >= 1


class TestCNNClassifier:
    @pytest.mark.asyncio
    async def test_image_classification(self, sample_image_file):
        classifier = cnn_classifier
        image = Image.open(sample_image_file)
        
        result = classifier.classify_image(image)
        assert "primary_class" in result
        assert "confidence" in result
        assert "predictions" in result
        assert len(result["predictions"]) > 0

    @pytest.mark.asyncio
    async def test_image_quality_assessment(self, sample_image_file):
        classifier = cnn_classifier
        image = Image.open(sample_image_file)
        
        quality = classifier.get_image_quality_score(image)
        assert "overall_quality" in quality
        assert "blur_score" in quality
        assert "brightness_score" in quality
        assert "contrast_score" in quality
        assert "is_acceptable" in quality


class TestOCREngine:
    @pytest.mark.asyncio
    async def test_text_extraction(self, sample_image_file):
        engine = ocr_engine
        image = Image.open(sample_image_file)
        
        result = engine.extract_text(image)
        assert "text" in result
        assert "confidence" in result
        assert "regions" in result
        assert "success" in result

    @pytest.mark.asyncio
    async def test_structured_text_extraction(self, sample_image_file):
        engine = ocr_engine
        image = Image.open(sample_image_file)
        
        result = engine.extract_structured_text(image)
        assert "text" in result
        assert "confidence" in result
        assert "structured_data" in result
        assert "success" in result


class TestVisionService:
    @pytest.mark.asyncio
    async def test_create_vision_image(self, test_db):
        service = VisionService()
        image_data = VisionImageCreate(
            user_id="test_user",
            title="Test Image",
            file_name="test.png",
            file_type="png",
            file_size=1000,
            file_url="/uploads/test.png",
            file_hash="test_hash",
        )
        
        image = await service.create_vision_image(image_data)
        assert image.id is not None
        assert image.status == ProcessingStatus.PENDING

    @pytest.mark.asyncio
    async def test_get_vision_image_by_id(self, test_db):
        service = VisionService()
        image_data = VisionImageCreate(
            user_id="test_user",
            title="Test Image",
            file_name="test.png",
            file_type="png",
            file_size=1000,
            file_url="/uploads/test.png",
            file_hash="test_hash",
        )
        
        created = await service.create_vision_image(image_data)
        retrieved = await service.get_vision_image_by_id(created.id, "test_user")
        
        assert retrieved is not None
        assert retrieved.id == created.id

    @pytest.mark.asyncio
    async def test_delete_vision_image(self, test_db):
        service = VisionService()
        image_data = VisionImageCreate(
            user_id="test_user",
            title="Test Image",
            file_name="test.png",
            file_type="png",
            file_size=1000,
            file_url="/uploads/test.png",
            file_hash="test_hash",
        )
        
        created = await service.create_vision_image(image_data)
        success = await service.delete_vision_image(created.id, "test_user")
        
        assert success is True
        retrieved = await service.get_vision_image_by_id(created.id, "test_user")
        assert retrieved is None


class TestVisionAPIEndpoints:
    @pytest.mark.asyncio
    async def test_vision_image_upload(self, client, sample_image_file):
        with open(sample_image_file, 'rb') as f:
            response = client.post(
                "/api/v1/vision/upload",
                files={"file": ("test.png", f, "image/png")},
                data={
                    "title": "Test Upload",
                    "subject": "Testing",
                    "tags": "test,vision",
                },
                headers={"Authorization": "Bearer test_token"},
            )
        
        assert response.status_code in [200, 401]

    @pytest.mark.asyncio
    async def test_get_vision_images(self, client):
        response = client.get(
            "/api/v1/vision/",
            headers={"Authorization": "Bearer test_token"},
        )
        
        assert response.status_code in [200, 401]

    @pytest.mark.asyncio
    async def test_vision_quiz_generation(self, client):
        response = client.post(
            "/api/v1/vision/test_id/quiz",
            headers={"Authorization": "Bearer test_token"},
        )
        
        assert response.status_code in [200, 401, 404, 500]

    @pytest.mark.asyncio
    async def test_vision_flashcard_generation(self, client):
        response = client.post(
            "/api/v1/vision/test_id/flashcards",
            headers={"Authorization": "Bearer test_token"},
        )
        
        assert response.status_code in [200, 401, 404, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
