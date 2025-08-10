# app/services/tts_service.py
import os
from openai import OpenAI

client = OpenAI()

def synthesize_tts(text: str, out_path: str, voice: str | None = None, fmt: str | None = "mp3"):
    """
    Uses OpenAI TTS (audio generation). Produces an audio file at out_path.
    Model names and parameters may vary by SDK/release.
    """
    if fmt not in ("mp3", "wav", "ogg"):
        fmt = "mp3"

    # Example call - adjust model name if needed
    # Many SDKs expose something like client.audio.speech.create(...)
    resp = client.audio.speech.create(
        model="gpt-4o-mini-tts",   # change if your account/model differs
        voice=voice or "alloy",   # optional
        input=text,
        format=fmt
    )
    # response may be binary, or contain a url/base64 depending on SDK.
    # Here assume `resp` contains bytes in resp.read() or .content
    # Try multiple approaches:
    if hasattr(resp, "read"):
        data = resp.read()
    elif hasattr(resp, "content"):
        data = resp.content
    elif isinstance(resp, bytes):
        data = resp
    elif isinstance(resp, dict) and "audio" in resp:
        # maybe base64 encoded
        import base64
        data = base64.b64decode(resp["audio"])
    else:
        # Try str extraction
        data = str(resp).encode("utf-8")

    with open(out_path, "wb") as f:
        f.write(data)
