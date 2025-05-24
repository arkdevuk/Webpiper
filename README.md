# 🗣️ Webpiper a simple TTS web-service

A simple, containerized web API for real-time text-to-speech (TTS) synthesis using [Piper](https://github.com/rhasspy/piper), powered by FastAPI.

## 🚀 Features

* 📥 Accepts text input and returns a synthesized speech `.wav` file
* 🧹 Automatically deletes audio files older than 1 hour
* 🎙️ Supports multiple languages and voice models (`.onnx`)
* 🪄 Apply custom audio effects via JSON-defined **effect chains**
* 🎛️ Effects include: `pitch_shift`, `normalize`, `flanger`, `random_semitone_sawtooth_wave` — with full parameter control
* 💾 Optionally convert output to **portable WAV format**:
  * Mono (1 channel)
  * 16-bit sample width
  * 48,000 Hz sample rate
* 🔐 Optional API key protection with HTTP Basic Auth (via `API_KEY` env variable)
* 📡 `/api/healthcheck` endpoint is always public for container monitoring
* 🐳 Built to run easily in Docker with configurable ports and bind-mounted output
* ⚡ Fast, lightweight, production-ready thanks to **FastAPI + Piper TTS**


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

## 🔐 Authentication (Optional)

You can protect your API with **Basic HTTP Authentication** by setting the `API_KEY` environment variable.

### ✅ Behavior

* If `API_KEY` is **not set** (default): all `/api/*` endpoints are publicly accessible.
* If `API_KEY` **is set**, then:

  * All `/api/*` routes **require Basic Auth**:

    * **Username**: `piper`
    * **Password**: your `API_KEY` value
  * The `/api/healthcheck` endpoint remains **public** for monitoring purposes.

### 🔧 Example

Set the environment variable when running the server:

```bash
export API_KEY=mysecurekey
uvicorn piper_tts_server:app --host 0.0.0.0 --port 8000
```

Then access the API like this:

```bash
curl -u piper:mysecurekey -X POST http://localhost:8000/api/v1/synthesize \
  -H "Content-Type: application/json" \
  -d '{ "text": "Bonjour !", "lite_file": true }'
```

If authentication fails, you'll receive:

```json
{
  "detail": "Unauthorized"
}
```

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
    environment:
      - API_KEY: mysecurekey # Optional - set API key for authentication
```

The API will be available at: [http://localhost:8080](http://localhost:8080)

---

## 🎨 Available Effects

You can chain multiple effects in the `effects` parameter.
Each effect has a `name` and optional `params` field.

| Effect Name                     | Description                                               | Parameters                                                             |
|---------------------------------|-----------------------------------------------------------| ---------------------------------------------------------------------- |
| `flanger`                       | Metallic flanger modulation                               | `rate`, `min_delay`, `max_delay`, `feedback`, `t_offset`, `dry`, `wet` |
| `pitch_shift`                   | Shifts the pitch up/down                                  | `pitch_change` (-100 to +100)                                          |
| `random_semitone_sawtooth_wave` | Applies a sawtooth modulation with random semitone shifts | `min_freq`, `max_semitones`, `pitch_duration`, `wet`                   |
| `normalize`                     | Removes DC offset & normalizes peak amplitude             | No parameters                                                          |
| `speed_change`                  | Changes the playback speed                                | `speed`                                                                  |

Example:

```json
{
  "effects": [
    { "name": "pitch_shift", "params": { "pitch_change": 10 } },
    { "name": "normalize", "params": {} }
  ]
}
```

## 🎨 Effects parameters

You can define a list of effects using the `effects` parameter in the request body.
Each effect should have a `name` and an optional `params` dictionary.

### 🔁 `flanger`

Applies a metallic-sounding flanger modulation.

**Parameters:**
* `rate` (float): LFO rate in Hz. Controls how fast the pitch shifts. Default: `0.15`
* `min_delay` (float): Minimum delay in seconds. Sets the starting point for the flanging. Default: `0.0025`
* `max_delay` (float): Maximum delay in seconds. Sets the depth of the flanging. Default: `0.0035`
* `feedback` (float): Amount of feedback (0 to 1). Higher values produce more intense echoes. Default: `0.9`
* `t_offset` (float): Static time offset for the modulation phase. Default: `0`
* `dry` (float): Dry (original) signal level. Range: `0` to `1`. Default: `0.5`
* `wet` (float): Wet (effected) signal level. Range: `0` to `1`. Default: `0.5`

---

### 🎚️ `normalize`

Removes DC offset and scales the audio to maximum amplitude.

**Parameters:**
* *(none)*

Note: Automatically centers the waveform and scales it to full 16-bit range.

---

### 🎼 `pitch_shift`

Changes the pitch of the audio without altering its duration.

**Parameters:**
* `pitch_change` (int): Pitch shift amount in semitone percent. Range: `-100` (one octave down) to `+100` (one octave up). Default: `0`

---

### 🎛️ `random_semitone_sawtooth_wave`

Applies amplitude modulation using a sawtooth wave with random semitone-based frequency changes.

**Parameters:**
* `min_freq` (float): Minimum frequency of the base sawtooth wave in Hz. Example: `170.0`
* `max_semitones` (int): Max number of semitones to shift up from `min_freq`. Higher = more variation.
* `pitch_duration` (float): Duration (in seconds) of each pitch modulation segment.
* `wet` (float): Strength of the effect (0 = no effect, 1 = full modulated signal). Default: `0.5`

---

### ⏩ speed_change

Changes the playback speed of the audio by resampling.

**Parameters:**
* `speed` (float): Speed adjustment factor. 
  * 0.0 = no change
  * Positive values speed up the audio (0.25 = 25% faster)
  * Negative values slow it down (-0.25 = 25% slower)
  * Range: around -0.9 to +1.0 is typical for experimental use

⚠️ This effect does alter the duration of the audio. It’s a simple and accurate time-domain resampling.

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

