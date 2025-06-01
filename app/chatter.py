import os
import queue
import threading
import time
import uuid

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from pathlib import Path

OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", "/output")).resolve()
VOICES_DIR = Path(os.getenv("VOICE_PATH", "/chattervoice")).resolve()

OUTPUT_DIR.mkdir(exist_ok=True)

file_queue = queue.Queue()


class Chatter:
    def __init__(self):
        self.model = None
        self.is_running = False

    def run_synchronously(self, text, voice=None, exaggeration=0.5, cfg_weight=0.5):
        filename = f"{uuid.uuid4().hex}.wav"
        output_path = OUTPUT_DIR / filename

        if voice is not None:
            voice = ChatterWrapper.find_voice(voice)

        if self.model is None:
            self.model = ChatterboxTTS.from_pretrained(device="cuda")

        wav = self.model.generate(text, audio_prompt_path=voice, exaggeration=exaggeration, cfg_weight=cfg_weight)
        ta.save(output_path, wav, self.model.sr)

        return output_path

    def add_message(self, text, voice=None, exaggeration=0.5, cfg_weight=0.5):
        message = {
            'text': text,
            'voice': voice,
            'exaggeration': exaggeration,
            'cfg_weight': cfg_weight
        }
        file_queue.put(message)
        self.is_running = True

    def process_loop(self):
        while self.is_running:
            if file_queue.empty():
                time.sleep(1)
                continue

            message = file_queue.get()
            if message is None:
                continue

            filename = f"{uuid.uuid4().hex}.wav"
            output_path = OUTPUT_DIR / filename

            if self.model is None:
                self.model = ChatterboxTTS.from_pretrained(device="cuda")
            if message.voice is None:
                wav = self.model.generate(message.text)
                ta.save(output_path, wav, self.model.sr)
            pass


class ChatterWrapper:
    def __init__(self):
        self.thread = None
        self.chatter = Chatter()
        # Start the processing thread
        self.thread = threading.Thread(target=self.chatter.process_loop, daemon=True).start()

    @staticmethod
    def find_voice(voice_name):
        # secure the voice name to prevent directory traversal attacks, remove / . %
        voice_name = voice_name.replace('/', '').replace('.', '').replace('%', '').replace('..', '').strip()
        voice_path = VOICES_DIR / f"{voice_name}.wav"
        if not voice_path.exists():
            raise FileNotFoundError(f"Voice file '{voice_name}' not found in {VOICES_DIR}")
        return str(voice_path)

    def add_message(self, text, voice=None, exaggeration=0.5, cfg_weight=0.5):
        self.chatter.add_message(text, voice, exaggeration, cfg_weight)

    def run_synchronously(self, text, voice=None, exaggeration=0.5, cfg_weight=0.5):
        return self.chatter.run_synchronously(text, voice, exaggeration, cfg_weight)