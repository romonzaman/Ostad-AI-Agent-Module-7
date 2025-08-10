# app/services/image_service.py
import base64
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def generate_image_from_prompt(prompt: str, out_path: str, width: int = 512, height: int = 512):
    """
    Uses OpenAI image generation API and writes PNG bytes to out_path.
    """
    # Example: client.images.generate(...) returns base64 data in many SDKs
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=f"{width}x{height}"
    )

    # resp could be dict with data[0].b64_json or similar
    # try common patterns:
    b64 = None
    if isinstance(resp, dict):
        # new style: resp["data"][0]["b64_json"]
        try:
            b64 = resp["data"][0]["b64_json"]
        except Exception:
            # older style: resp["data"][0]["b64"]
            try:
                b64 = resp["data"][0]["b64"]
            except Exception:
                pass
    else:
        # some client libs return an object with .data attribute
        try:
            b64 = resp.data[0].b64_json
        except Exception:
            pass

    if not b64:
        raise RuntimeError("Unexpected image response format; cannot find base64 image data")

    img_bytes = base64.b64decode(b64)
    with open(out_path, "wb") as f:
        f.write(img_bytes)
