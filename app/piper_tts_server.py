import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from tts import synthesize_text
from audio_utils import to_portable_file
from audio_file_utils import AudioFileUtils
from effects.chain_processor import EffectChainProcessor

SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", "/output")).resolve()

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
    effects: Optional[List[Dict[str, Any]]] = None
    lite_file: Optional[bool] = False

@app.post("/api/v1/synthesize")
async def synthesize(req: SynthesizeRequest):
    try:
        # TTS synthesis
        output_file = synthesize_text(
            text=req.text,
            local=req.local,
            voice=req.voice,
            silence=req.silence,
            speed=req.speed,
            noise_w=req.noise_w
        )

        # Effects chain processing
        if req.effects:
            audio, framerate = AudioFileUtils.wav_to_audio(output_file)
            processor = EffectChainProcessor()
            audio = processor.apply_chain(audio, framerate, req.effects)
            AudioFileUtils.audio_to_wav(audio, framerate, output_file)

        # Lite file conversion
        if req.lite_file:
            to_portable_file(output_file, output_file)

        # Response
        filename = Path(output_file).name
        return JSONResponse(
            status_code=200,
            content={
                "filename": filename,
                "url": f"/api/v1/synthesize/{filename}"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/synthesize/{filename}")
async def get_audio_file(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="audio/wav")

@app.get("/api/healthcheck")
async def healthcheck():
    return {"status": "ok"}

# Run with: uvicorn piper_tts_server:app --host 0.0.0.0 --port $SERVER_PORT
