Here’s your **updated README.md**, documenting the new parameters (`effects`, `lite_file`) and how to use the effect chains via JSON:

---

# 🗣️ Piper TTS Web Server

A simple, containerized web API for real-time text-to-speech (TTS) synthesis using [Piper](https://github.com/rhasspy/piper), powered by FastAPI.

## 🚀 Features

* 📥 Accepts text input and returns a synthesized speech `.wav` file
* 🧹 Automatically deletes audio files older than 1 hour
* 🎙️ Supports multiple voices and languages
* 🪄 Apply custom audio effects via JSON-defined effect chains
* 💾 Optionally convert output files to portable 16-bit mono WAV format
* 📡 Healthcheck endpoint for easy container monitoring
* 🔌 Built to run in Docker with configurable ports

---

## 📦 API Endpoints

### `POST /api/v1/synthesize`

Synthesize speech from text with optional effects.

#### Request Body (JSON):

```json
{
  "text": "Hello, world!",
  "local": "fr_FR",                    // Optional - default: "fr_FR"
  "voice": "siwis-medium",             // Optional - default: "siwis-medium"
  "silence": 1,                        // Optional - sentence silence (seconds)
  "speed": 1.0,                        // Optional - speech speed factor
  "noise_w": 0.8,                      // Optional - noise weight
  "effects": [                         // Optional - list of effect steps to apply
    {
      "name": "pitch_shift",
      "params": { "pitch_change": 10 }
    },
    {
      "name": "random_semitone_sawtooth_wave",
      "params": { "min_freq": 170, "max_semitones": 6, "pitch_duration": 0.4, "wet": 0.3 }
    },
    {
      "name": "normalize",
      "params": {}
    }
  ],
  "lite_file": true                    // Optional - convert to 16-bit mono WAV
}
```

#### Success Response (200):

```json
{
  "filename": "abcd1234.wav",
  "url": "/api/v1/synthesize/abcd1234.wav"
}
```

---

### `GET /api/v1/synthesize/<filename>`

Download a previously synthesized `.wav` file.

---

### `GET /api/healthcheck`

Simple healthcheck for the server.

---

## 🐳 Running with Docker

### Use with Docker compose

```yaml
services:
  piper-tts:
    image: arkdevuk/webpiper:latest
    container_name: piper-tts
    ports:
      - "8080:8080" # exposed port : container port, you can change the exposed port if needed
    volumes:
      - ./output:/output         # Mount output directory to access generated audio
    restart: unless-stopped
```

The API will be available at: [http://localhost:8080](http://localhost:8080)

---

## 🎨 Available Effects

You can chain multiple effects in the `effects` parameter.
Each effect has a `name` and optional `params` field.

| Effect Name                     | Description                                               | Parameters                                                             |
| ------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------- |
| `flanger`                       | Metallic flanger modulation                               | `rate`, `min_delay`, `max_delay`, `feedback`, `t_offset`, `dry`, `wet` |
| `pitch_shift`                   | Shifts the pitch up/down                                  | `pitch_change` (-100 to +100)                                          |
| `random_semitone_sawtooth_wave` | Applies a sawtooth modulation with random semitone shifts | `min_freq`, `max_semitones`, `pitch_duration`, `wet`                   |
| `normalize`                     | Removes DC offset & normalizes peak amplitude             | No parameters                                                          |

Example:

```json
"effects": [
  { "name": "pitch_shift", "params": { "pitch_change": 10 } },
  { "name": "normalize", "params": {} }
]
```

---

## 🎤 Voice Models

Piper voice files (`.onnx`) are stored in `/voices`.

You can find voice models here:
👉 [https://github.com/rhasspy/piper/blob/master/VOICES.md](https://github.com/rhasspy/piper/blob/master/VOICES.md)

Download and place them inside the `voices/` folder.
They should be named like: `fr_FR-siwis-medium.onnx`.

---

## 🛠️ Requirements

* Python 3.10
* FastAPI
* Uvicorn
* Piper TTS Engine

Install with:

```bash
pip install -r requirements.txt
```

---

## 📃 License

MIT License

---

## 🙌 Acknowledgements

* [Piper](https://github.com/rhasspy/piper) - Lightweight, fast TTS engine
* [FastAPI](https://fastapi.tiangolo.com/) - High performance web framework
* [Voicebox](https://voicebox.readthedocs.io/en/stable/index.html) - Inspiration to build the effects feature

