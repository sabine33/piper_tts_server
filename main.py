# main.py
import io
import wave
from fastapi import FastAPI, Form, Response
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from piper import PiperVoice


app = FastAPI()

# Allow CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Piper voice model once at startup
VOICE_PATH = "./models/en_US-hfc_male-medium.onnx"  # Change to your model path
voice = PiperVoice.load(VOICE_PATH)


@app.post("/synthesize")
async def synthesize(text: str = Form(...)):
    with wave.open("test.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    return StreamingResponse(
        open("test.wav", "rb"),
        media_type="audio/wav",
        headers={"Content-Disposition": "inline; filename=output.wav"},
    )

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        return f.read()
