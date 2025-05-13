import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from tts import synthesize_text, cleanup_old_files, OUTPUT_DIR, TTSException

SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SynthesizeRequest(BaseModel):
    text: str
    local: Optional[str] = "fr_FR"
    voice: Optional[str] = "siwis-medium"
    silence: Optional[int] = 1
    speed: Optional[float] = 1.0
    noise_w: Optional[float] = 0.8

@app.post("/api/v1/synthesize")
async def synthesize(req: SynthesizeRequest):
    cleanup_old_files()

    try:
        audio_file = synthesize_text(
            text=req.text,
            local=req.local,
            voice=req.voice,
            silence=req.silence,
            speed=req.speed,
            noise_w=req.noise_w
        )
    except TTSException as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(
        status_code=200,
        content={
            "filename": audio_file.name,
            "url": f"/api/v1/synthesize/{audio_file.name}"
        }
    )

@app.get("/api/v1/synthesize/{filename}")
async def get_audio_file(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="audio/wav")

@app.get("/api/healthcheck")
async def healthcheck():
    return {"status": "ok"}

# Run with: uvicorn main:app --host 0.0.0.0 --port $SERVER_PORT
