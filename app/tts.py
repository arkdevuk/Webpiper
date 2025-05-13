import os
import uuid
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", "/output")).resolve()
VOICES_DIR = Path(os.getenv("VOICE_PATH", "/voice")).resolve()

OUTPUT_DIR.mkdir(exist_ok=True)

class TTSException(Exception):
    pass

def cleanup_old_files(hours: int = 1):
    one_hour_ago = datetime.now() - timedelta(hours=hours)
    for file in OUTPUT_DIR.glob("*.wav"):
        if datetime.fromtimestamp(file.stat().st_mtime) < one_hour_ago:
            file.unlink()

def synthesize_text(
    text: str,
    local: str = "fr_FR",
    voice: str = "siwis-medium",
    silence: int = 1,
    speed: float = 1.0,
    noise_w: float = 0.8
) -> Path:
    filename = f"{uuid.uuid4().hex}.wav"
    output_path = OUTPUT_DIR / filename

    model_path = VOICES_DIR / f"{local}-{voice}.onnx"

    if not model_path.exists():
        raise TTSException(f"Voice model not found: {model_path}")

    try:
        subprocess.run(
            [
                "piper",
                "--model", str(model_path),
                "--output_file", str(output_path),
                "--sentence-silence", str(silence),
                "--length_scale", str(speed),
                "--noise_w", str(noise_w),
            ],
            input=text.encode("utf-8"),
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise TTSException("Synthesis failed") from e

    return output_path
