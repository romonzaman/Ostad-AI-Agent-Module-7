# app/routes/tts.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import uuid
from app.services.tts_service import synthesize_tts

router = APIRouter()
TMP_DIR = Path("tmp")
TMP_DIR.mkdir(exist_ok=True)

class TTSRequest(BaseModel):
    text: str
    voice: str | None = None  # optional voice param if provider supports it
    format: str | None = "mp3"  # mp3 or wav

@router.post("/", summary="Synthesize speech from text")
async def tts_endpoint(req: TTSRequest):
    if not req.text:
        raise HTTPException(status_code=400, detail="Text is empty")
    out_path = TMP_DIR / f"{uuid.uuid4().hex}.{req.format or 'mp3'}"
    try:
        synthesize_tts(req.text, str(out_path), voice=req.voice, fmt=req.format)
        return FileResponse(path=str(out_path), filename=f"tts.{req.format}", media_type="audio/mpeg" if req.format=="mp3" else "audio/wav")
    finally:
        # keep file for client to download; optionally schedule cleanup
        pass
