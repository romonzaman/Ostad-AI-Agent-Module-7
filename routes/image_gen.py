# app/routes/image_gen.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import uuid
from app.services.image_service import generate_image_from_prompt

router = APIRouter()
TMP_DIR = Path("tmp")
TMP_DIR.mkdir(exist_ok=True)

class ImageGenRequest(BaseModel):
    prompt: str
    width: int | None = 512
    height: int | None = 512

@router.post("/", summary="Generate image from prompt")
async def generate_image(req: ImageGenRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt is empty")
    out_path = TMP_DIR / f"{uuid.uuid4().hex}.png"
    generate_image_from_prompt(req.prompt, str(out_path), width=req.width, height=req.height)
    return FileResponse(path=str(out_path), filename="generated.png", media_type="image/png")
