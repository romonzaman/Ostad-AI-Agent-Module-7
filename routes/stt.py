# app/routes/stt.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
from app.services.stt_service import transcribe_file

router = APIRouter()
TMP_DIR = Path("tmp")
TMP_DIR.mkdir(exist_ok=True)

@router.post("/", summary="Transcribe uploaded audio file")
async def stt_endpoint(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Missing file.")
    # save to tmp
    tmp_path = TMP_DIR / f"{uuid.uuid4().hex}_{file.filename}"
    try:
        with open(tmp_path, "wb") as f:
            f.write(await file.read())
        transcription = transcribe_file(str(tmp_path))
        return JSONResponse({"transcription": transcription})
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except:
            pass
