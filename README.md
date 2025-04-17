# 🗣️ Piper TTS Web Server

A simple, containerized web API for real-time text-to-speech (TTS) synthesis using [Piper](https://github.com/rhasspy/piper), powered by FastAPI.

## 🚀 Features

- 📥 Accepts text input and returns a synthesized speech `.wav` file
- 🧹 Automatically deletes audio files older than 1 hour
- 📡 Healthcheck endpoint for easy container monitoring
- 🎙️ Supports multiple voices and languages
- 🔌 Built to run in Docker with configurable ports

---

## 📦 API Endpoints

### `POST /api/v1/synthesize`

Synthesize speech from text.

#### Request Body (JSON):
```json
{
  "text": "Hello, world!",
  "local": "fr_FR",      // Optional - default: "fr_FR"
  "voice": "siwis-medium" // Optional - default: "siwis-medium"
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

### 1. Clone the repo and build the image:

```bash
git clone https://github.com/your-username/piper-tts-server.git
cd piper-tts-server
docker build -t piper-tts-server .
```

### 2. Run the container:

```bash
docker run -p 8080:8080 \
  -e SERVER_PORT=8080 \
  piper-tts-server
```

The API will be available at: [http://localhost:8080](http://localhost:8080)

---

## 🗂️ Project Structure

```
.
├── app/
│   ├── piper_tts_server.py     # FastAPI app
│   └── requirements.txt        # Python dependencies
├── voices/                     # Voice models (.onnx)
├── output/                     # Synthesized .wav files (auto-created)
├── Dockerfile
└── README.md
```

---

## 🎤 Voice Models

Piper voice files (`.onnx`) are stored in `/voice`.

You can find voice models here:  
👉 https://github.com/rhasspy/piper/blob/master/VOICES.md

Download and place them inside the `voices/` folder.  
They should be named like: `fr_FR-siwis-medium.onnx`.

---

## 🛠️ Requirements

- Python 3.10
- FastAPI
- Uvicorn
- Piper TTS Engine

Install with:

```bash
pip install -r requirements.txt
```

---

## 📃 License

MIT License

---

## 🙌 Acknowledgements

- [Piper](https://github.com/rhasspy/piper) - Lightweight, fast TTS engine
- [FastAPI](https://fastapi.tiangolo.com/) - High performance web framework
