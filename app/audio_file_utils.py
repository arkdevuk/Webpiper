import wave
import numpy as np
from pathlib import Path

class AudioFileUtils:
    @staticmethod
    def wav_to_audio(filepath: Path):
        with wave.open(str(filepath), 'rb') as wf:
            nchannels, sampwidth, framerate, nframes, _, _ = wf.getparams()
            if nchannels != 1:
                raise ValueError("Only mono WAV files are supported")

            frames = wf.readframes(nframes)
            audio = np.frombuffer(frames, dtype=np.int16)

        return audio.astype(np.float32), framerate

    @staticmethod
    def audio_to_wav(audio: np.ndarray, framerate: int, output_path: Path):
        # Ensure correct format
        audio_clipped = np.clip(audio, -32768, 32767).astype(np.int16)

        with wave.open(str(output_path), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(framerate)
            wf.writeframes(audio_clipped.tobytes())
