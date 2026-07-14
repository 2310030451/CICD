import pytest
from app.ai.voice import VoiceAI
import tempfile
import os


@pytest.fixture
async def voice_ai():
    return VoiceAI()


class TestVoiceAI:
    @pytest.mark.asyncio
    async def test_voice_ai_initialization(self, voice_ai):
        """Test Voice AI initialization"""
        assert voice_ai is not None
        assert voice_ai.model_size == "base"
        
    @pytest.mark.asyncio
    async def test_load_whisper_model(self, voice_ai):
        """Test Whisper model loading"""
        model = voice_ai.load_whisper_model()
        assert model is not None
        
    @pytest.mark.asyncio
    async def test_get_supported_languages(self, voice_ai):
        """Test getting supported languages"""
        languages = voice_ai.get_supported_languages()
        assert isinstance(languages, dict)
        assert "en" in languages
        assert "es" in languages
        assert "hi" in languages
        
    @pytest.mark.asyncio
    async def test_get_whisper_languages(self, voice_ai):
        """Test getting Whisper supported languages"""
        languages = voice_ai.get_whisper_languages()
        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "en" in languages
        assert "es" in languages
        
    @pytest.mark.asyncio
    async def test_text_to_speech(self, voice_ai):
        """Test text-to-speech conversion"""
        text = "Hello, this is a test."
        audio_data = await voice_ai.text_to_speech(text, language="en")
        assert audio_data is not None
        assert isinstance(audio_data, bytes)
        assert len(audio_data) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
