# --- Audio Transcription and Alignment Logic -------------------------------
import streamlit as st
from google.genai import types
from .utils import clean_transcription, remove_timestamps
import prompts

# --- Audio Transcription ---------------------------------------------------
def transcribe_audio(audio_file, is_teacher: bool, client, config) -> str:
    """
    Transcribe audio file using Gemini API
    
    Args:
        audio_file: Uploaded audio file from Streamlit
        is_teacher: True for teacher audio, False for observer audio
        client: Gemini API client
        config: Generation configuration
    
    Returns:
        Transcription text
    """
    try:
        # Reset file pointer and read bytes
        audio_file.seek(0)
        audio_bytes = audio_file.read()
        
        # Validate file is not empty
        if len(audio_bytes) == 0:
            raise ValueError(f"{'Teacher' if is_teacher else 'Observer'} audio file is empty or corrupted")
        
        # Create audio part
        file_extension = audio_file.name.split('.')[-1]
        audio_part = types.Part.from_bytes(
            data=audio_bytes, 
            mime_type=f"audio/{file_extension}"
        )
        
        # Select appropriate prompt
        prompt = prompts.TEACHER_TRANSCRIPTION_PROMPT if is_teacher else prompts.OBSERVER_TRANSCRIPTION_PROMPT
        
        # Generate transcription
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=[types.Part(text=prompt), audio_part])],
            config=config,
        )
        
        return response.text
        
    except Exception as e:
        raise Exception(f"{'Teacher' if is_teacher else 'Observer'} transcription failed: {str(e)}")


# --- Transcription Alignment -----------------------------------------------
def align_transcriptions(teacher_text: str, observer_content: str, client, config) -> tuple[str, str]:
    """
    Align teacher and observer transcriptions chronologically
    
    Args:
        teacher_text: Teacher audio transcription
        observer_content: Observer audio/notes content
        client: Gemini API client
        config: Generation configuration
    
    Returns:
        Tuple of (aligned_teacher, aligned_observer)
    """
    try:
        # Clean transcriptions first
        teacher_text = clean_transcription(teacher_text)
        observer_content = clean_transcription(observer_content) if observer_content else ""
        
        # If no observer content, just remove timestamps from teacher
        if not observer_content:
            return remove_timestamps(teacher_text), ""
        
        # Generate alignment prompt
        alignment_prompt = prompts.get_alignment_prompt(teacher_text, observer_content)
        
        # Attempt alignment via API
        result_text = ""
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=[types.Content(parts=[types.Part(text=alignment_prompt)])],
                config=config,
            )
            if hasattr(response, 'text') and response.text:
                result_text = response.text
        except:
            result_text = ""
        
        # Parse alignment result
        if result_text and "ALIGNED_TEACHER:" in result_text and "ALIGNED_OBSERVER:" in result_text:
            parts = result_text.split("ALIGNED_OBSERVER:")
            teacher_part = parts[0].replace("ALIGNED_TEACHER:", "").strip()
            observer_part = parts[1].strip()
            aligned_teacher = clean_transcription(teacher_part)
            aligned_observer = clean_transcription(observer_part)
        else:
            # Fallback: Just remove timestamps
            aligned_teacher = remove_timestamps(teacher_text)
            aligned_observer = remove_timestamps(observer_content)
        
        return aligned_teacher, aligned_observer
        
    except Exception as e:
        # Fallback on error: remove timestamps and return
        return remove_timestamps(teacher_text), remove_timestamps(observer_content)
