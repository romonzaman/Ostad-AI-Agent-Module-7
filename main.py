# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stt, tts, image_gen

app = FastAPI(title="Multimodal API (OpenAI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stt.router, prefix="/stt", tags=["stt"])
app.include_router(tts.router, prefix="/tts", tags=["tts"])
app.include_router(image_gen.router, prefix="/generate-image", tags=["image_gen"])

@app.get("/")
async def root():
    return {"message": "Multimodal API (OpenAI) - alive"}
