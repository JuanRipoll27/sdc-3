"""FastAPI service for StyleLab image transformations."""

import io

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError

import config
import inference


app = FastAPI(
    title="StyleLab API",
    description="Apply pre-trained artistic styles to uploaded photos.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to StyleLab API", "docs": "/docs"}


@app.get("/health")
def health():
    """Simple check that the FastAPI service is responding."""
    return {"status": "ok", "service": "stylelab-backend"}


@app.get("/styles")
def available_styles():
    """The frontend reads this list instead of keeping its own copy."""
    return {"styles": list(config.STYLES.keys())}


@app.post(
    "/{style}",
    responses={200: {"content": {"image/png": {}}, "description": "Stylized PNG image"}},
)
async def transform_image(
    style: str,
    file: UploadFile = File(...),
    strength: float = Form(1.0, ge=0.0, le=1.0),
):
    """Transform an image and optionally blend it with the original.

    strength=0.0 means original photo; strength=1.0 means full style.
    """
    if style not in config.STYLES:
        raise HTTPException(status_code=404, detail="Unknown artistic style")

    try:
        # Pillow reads RGB; OpenCV processes BGR.
        original_rgb = Image.open(file.file).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Upload a valid image") from exc
    finally:
        await file.close()

    original_bgr = cv2.cvtColor(np.array(original_rgb), cv2.COLOR_RGB2BGR)

    # Existing model inference from the original course exercise.
    stylized, resized_original = inference.inference(
        config.STYLES[style], original_bgr
    )

    # Inference outputs float pixels: convert them to valid PNG pixels.
    stylized = np.clip(stylized, 0, 255).astype(np.uint8)

    # Neural style models may round the width to a multiple of 4.
    # Resize their output to the input preview dimensions before blending.
    if stylized.shape[:2] != resized_original.shape[:2]:
        stylized = cv2.resize(
            stylized,
            (resized_original.shape[1], resized_original.shape[0]),
            interpolation=cv2.INTER_LINEAR,
        )

    # Blend two equal-size BGR images (no new AI model is involved).
    blended = cv2.addWeighted(
        resized_original, 1.0 - strength, stylized, strength, 0
    )
    ok, encoded = cv2.imencode(".png", blended)
    if not ok:
        raise HTTPException(status_code=500, detail="Could not encode the image")

    return Response(content=encoded.tobytes(), media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80)
