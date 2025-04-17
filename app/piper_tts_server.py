# inspiration : https://github.com/peteh/mary-piper
# I have installed on this container a Python package called `piper` that is a TTS engine.
# echo 'Welcome to the world of speech synthesis!' | \
#    ./piper --model en_US-lessac-medium.onnx --output_file welcome.wav
# I want to create a simple web server that will take a text input and generate a speech audio file using the piper TTS engine.
# It will return a link to the audio file
# it has 3 endpoints:
# 1. /api/v1/synthesize: POST request with JSON body containing the text to synthesize
# on each call to this route the script will delete file older than 1 hour
#       Params :
#          - text: the text to synthesize
#          - local: the local voice file to use (default is fr_FR)
#          - voice: the voice file to use (default is siwis-medium)
#       Returns:
#          - 200 OK: if the synthesis was successful :
#              - filename : the name of the audio file
#              - url : the url to download the audio file /api/v1/synthesize/<filename>
#          - 400 Bad Request: if the synthesis failed
# 2. /api/v1/synthesize/<filename>: GET request to download the audio file
# The audio file will be saved in the (absolute)/output directory
# the voice file are stored in (absolute)/voices directory
# 3. /api/healthcheck: GET request to check if the server is running
#
# Port will be set using SERVER_PORT
# The server will be running on http://0.0.0.0:<SERVER_PORT>, as docker will handle the port mapping

import os
import uuid
import shutil
import subprocess
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import glob

# Config
SERVER_PORT = int(os.getenv("SERVER_PORT", 8080))
OUTPUT_DIR = "/output"
VOICES_DIR = "/voices"

OUTPUT_DIR.mkdir(exist_ok=True)

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class SynthesizeRequest(BaseModel):
    text: str
    local: Optional[str] = "fr_FR"
    voice: Optional[str] = "siwis-medium"

# Cleanup function to delete files older than 1 hour
def cleanup_old_files():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    for file in OUTPUT_DIR.glob("*.wav"):
        if datetime.fromtimestamp(file.stat().st_mtime) < one_hour_ago:
            file.unlink()

# Synthesize endpoint
@app.post("/api/v1/synthesize")
async def synthesize(req: SynthesizeRequest):
    cleanup_old_files()

    filename = f"{uuid.uuid4().hex}.wav"
    output_path = OUTPUT_DIR / filename

    model_path = VOICES_DIR / f"{req.local}-{req.voice}.onnx"

    if not model_path.exists():
        raise HTTPException(status_code=400, detail="Voice model not found")

    try:
        subprocess.run(
            [
                "piper",
                "--model", str(model_path),
                "--output_file", str(output_path),
            ],
            input=req.text.encode("utf-8"),
            check=True
        )
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=400, detail="Synthesis failed")

    return JSONResponse(
        status_code=200,
        content={
            "filename": filename,
            "url": f"/api/v1/synthesize/{filename}"
        }
    )

# File download endpoint
@app.get("/api/v1/synthesize/{filename}")
async def get_audio_file(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="audio/wav")

# Healthcheck endpoint
@app.get("/api/healthcheck")
async def healthcheck():
    return {"status": "ok"}

# Run with: uvicorn piper_server:app --host 0.0.0.0 --port $SERVER_PORT
