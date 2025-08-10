# app/services/stt_service.py
import os
from pathlib import Path
from openai import OpenAI

# expect OPENAI_API_KEY in env
client = OpenAI()

def transcribe_file(filepath: str) -> str:
    """
    Uses OpenAI speech-to-text (transcription) API.
    Adjust model name if necessary.
    """
    # read binary file
    with open(filepath, "rb") as audio_file:
        # Using the modern client: client.audio.transcriptions.create(...)
        # adjust if your installed SDK uses openai.Audio.transcribe(...) older API
        resp = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",  # or change to available transcribe model
            file=audio_file
        )
    # resp is expected to have 'text' field
    text = getattr(resp, "text", None) or resp.get("text") if isinstance(resp, dict) else None
    if text is None:
        # fallback: try resp['data'][0]['text']
        try:
            text = resp["data"][0]["text"]
        except Exception:
            raise RuntimeError("Unexpected transcription response format")
    return text.strip()
