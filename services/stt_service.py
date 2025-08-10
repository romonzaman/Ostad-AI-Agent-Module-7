# app/services/stt_service.py
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


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
    text = getattr(resp, "text", None)
    if not text:
        # fallback: try str() or raise error
        raise RuntimeError("Unexpected transcription response format: no text found")

    return text.strip()
