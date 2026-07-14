from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import tempfile
import os
import io
from loguru import logger
from app.ai.voice import voice_ai

router = APIRouter()

@router.post("/speech-to-text")
async def speech_to_text(
    audio_file: UploadFile = File(...),
    language: Optional[str] = None
):
    """
    Convert speech audio to text using Whisper
    
    Args:
        audio_file: Audio file (mp3, wav, m4a, etc.)
        language: Language code (e.g., 'en', 'es', 'hi'). If None, auto-detect.
    
    Returns:
        Transcription with metadata
    """
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Transcribe audio
        result = await voice_ai.speech_to_text(temp_path, language)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        logger.error(f"Speech-to-text error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text-to-speech")
async def text_to_speech(
    text: str,
    language: str = "en",
    slow: bool = False
):
    """
    Convert text to speech using gTTS
    
    Args:
        text: Text to convert
        language: Language code (e.g., 'en', 'es', 'hi')
        slow: Whether to speak slowly
    
    Returns:
        Audio file (MP3)
    """
    try:
        audio_data = await voice_ai.text_to_speech(text, language, slow)
        
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
    
    except Exception as e:
        logger.error(f"Text-to-speech error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_supported_languages():
    """
    Get supported languages for voice features
    
    Returns:
        Dict of supported languages
    """
    return {
        "text_to_speech": voice_ai.get_supported_languages(),
        "speech_to_text": voice_ai.get_whisper_languages()
    }
