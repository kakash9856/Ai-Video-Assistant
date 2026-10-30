

import os
import whisper

# FFmpeg path for Windows
FFMPEG_PATH = (
    r"C:\Users\kakas\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build\bin"
)

# Add FFmpeg to Python PATH
os.environ["PATH"] = (
    FFMPEG_PATH + os.pathsep + os.environ.get("PATH", "")
)

# Whisper model
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

_model = None


def load_model():
    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}...", flush=True)
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.", flush=True)

    return _model


def transcribe_chunk_whisper(chunk_path: str) -> str:
    print("Starting transcription...", flush=True)
    print("Audio file:", chunk_path, flush=True)

    if not os.path.exists(chunk_path):
        raise FileNotFoundError(f"Audio file not found: {chunk_path}")

    model = load_model()

    result = model.transcribe(
        chunk_path,
        task="transcribe",
        fp16=False,
        verbose=False
    )

    text = result["text"].strip()

    print("Transcription completed!", flush=True)

    return text


def transcribe_all(chunks: list, language: str = "english") -> str:
    transcripts = []

    for i, chunk_path in enumerate(chunks, start=1):
        print(
            f"Transcribing chunk {i}/{len(chunks)}...",
            flush=True
        )

        text = transcribe_chunk_whisper(chunk_path)
        transcripts.append(text)

    print("All chunks transcribed successfully!", flush=True)

    return "\n\n".join(transcripts)
