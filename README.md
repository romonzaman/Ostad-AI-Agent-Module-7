# Multimodal API (FastAPI)

Provides three endpoints:
- `POST /stt/` : upload audio (`multipart/form-data`) -> returns JSON transcription
- `POST /tts/` : JSON `{ "text": "..." }` -> returns `audio/wav`
- `POST /generate-image/` : JSON `{ "prompt": "..." }` -> returns `image/png`

## Setup (example)
1. Create and activate a virtualenv
   ```bash
   python -m venv venv
   source venv/bin/activate
