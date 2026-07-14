import io
import tempfile
import os
from typing import Optional, Dict
from loguru import logger
from app.config import settings

class VoiceAI:
    """Voice AI service for speech-to-text and text-to-speech"""
    
    def __init__(self):
        self._initialized = False
        self.whisper_model = None
        self.model_size = "base"  # Options: tiny, base, small, medium, large
    
    def _ensure_initialized(self):
        """Lazy initialization to avoid startup errors"""
        if self._initialized:
            return
        try:
            import whisper
            self.whisper_model = whisper.load_model(self.model_size)
            logger.info(f"Whisper model loaded: {self.model_size}")
            self._initialized = True
        except ImportError as e:
            logger.error(f"Whisper not available: {e}")
            self._initialized = False
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self._initialized = False
    
    def load_whisper_model(self):
        """Load Whisper model for speech-to-text"""
        self._ensure_initialized()
        return self.whisper_model
    
    async def speech_to_text(self, audio_file_path: str, language: Optional[str] = None) -> Dict:
        """
        Convert speech audio to text using Whisper
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (e.g., 'en', 'es', 'hi'). If None, auto-detect.
        
        Returns:
            Dict with transcription and metadata
        """
        try:
            self._ensure_initialized()
            
            if not self._initialized:
                raise RuntimeError("Whisper model is not available")
                
            import whisper
            model = self.whisper_model or whisper.load_model(self.model_size)
            
            # Transcribe audio
            result = model.transcribe(
                audio_file_path,
                language=language,
                fp16=False  # Use FP32 for better compatibility
            )
            
            return {
                "text": result["text"],
                "language": result.get("language", "unknown"),
                "segments": result.get("segments", []),
                "duration": result.get("duration", 0)
            }
        
        except Exception as e:
            logger.error(f"Speech-to-text failed: {e}")
            raise
    
    async def text_to_speech(self, text: str, language: str = "en", slow: bool = False) -> bytes:
        """
        Convert text to speech using gTTS
        
        Args:
            text: Text to convert
            language: Language code (e.g., 'en', 'es', 'hi')
            slow: Whether to speak slowly
        
        Returns:
            Audio data as bytes
        """
        try:
            from gtts import gTTS
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_path = temp_file.name
            
            tts.save(temp_path)
            
            # Read audio file
            with open(temp_path, "rb") as f:
                audio_data = f.read()
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return audio_data
        
        except Exception as e:
            logger.error(f"Text-to-speech failed: {e}")
            raise
    
    async def text_to_speech_stream(self, text: str, language: str = "en", slow: bool = False):
        """
        Stream text-to-speech audio
        
        Args:
            text: Text to convert
            language: Language code
            slow: Whether to speak slowly
        
        Yields:
            Audio chunks
        """
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang=language, slow=slow)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_path = temp_file.name
            
            tts.save(temp_path)
            
            # Stream audio in chunks
            with open(temp_path, "rb") as f:
                while chunk := f.read(4096):
                    yield chunk
            
            os.unlink(temp_path)
        
        except Exception as e:
            logger.error(f"Text-to-speech stream failed: {e}")
            raise
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages for text-to-speech"""
        return {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "hi": "Hindi",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "ar": "Arabic",
            "ru": "Russian"
        }
    
    def get_whisper_languages(self) -> list:
        """Get languages supported by Whisper"""
        # Whisper supports 99 languages
        return [
            "en", "es", "fr", "de", "it", "pt", "nl", "ru", "zh", "ja",
            "ko", "hi", "ar", "tr", "pl", "sv", "uk", "el", "cs", "ro",
            "da", "fi", "hu", "id", "ms", "th", "vi", "bn", "ta", "te",
            "mr", "ur", "fa", "he", "yo", "sw", "zu"
        ]

# Global Voice AI instance
voice_ai = VoiceAI()
