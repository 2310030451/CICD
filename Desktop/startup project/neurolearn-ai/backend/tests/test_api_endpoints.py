import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
async def client():
    async with TestClient(app) as test_client:
        yield test_client


class TestHealthEndpoints:
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestDocumentEndpoints:
    def test_get_documents_unauthorized(self, client):
        response = client.get("/api/v1/documents/")
        assert response.status_code in [401, 403]
        
    def test_upload_document_unauthorized(self, client):
        response = client.post("/api/v1/documents/upload")
        assert response.status_code in [401, 403, 422]


class TestChatEndpoints:
    def test_chat_unauthorized(self, client):
        response = client.post("/api/v1/ai/chat", json={"question": "test"})
        assert response.status_code in [401, 403, 422]
        
    def test_get_conversations_unauthorized(self, client):
        response = client.get("/api/v1/ai/conversations")
        assert response.status_code in [401, 403]


class TestVisionEndpoints:
    def test_vision_upload_unauthorized(self, client):
        response = client.post("/api/v1/vision/upload")
        assert response.status_code in [401, 403, 422]


class TestVoiceEndpoints:
    def test_speech_to_text_unauthorized(self, client):
        response = client.post("/api/v1/voice/speech-to-text")
        assert response.status_code in [401, 403, 422]
        
    def test_text_to_speech_unauthorized(self, client):
        response = client.post("/api/v1/voice/text-to-speech")
        assert response.status_code in [401, 403, 422]
        
    def test_get_languages(self, client):
        response = client.get("/api/v1/voice/languages")
        assert response.status_code == 200
        data = response.json()
        assert "text_to_speech" in data
        assert "speech_to_text" in data


class TestMonitoringEndpoints:
    def test_monitoring_health(self, client):
        response = client.get("/api/v1/monitoring/health")
        assert response.status_code == 200
        
    def test_monitoring_metrics(self, client):
        response = client.get("/api/v1/monitoring/metrics")
        assert response.status_code == 200
        
    def test_monitoring_summary(self, client):
        response = client.get("/api/v1/monitoring/metrics/summary")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
