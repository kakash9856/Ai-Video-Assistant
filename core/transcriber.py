
import os
import whisper

# Whisper model: tiny, base, small, medium, large
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.")

    return _model


def transcribe_chunk_whisper(chunk_path: str) -> str:
    model = load_model()

    result = model.transcribe(
        chunk_path,
        task="transcribe",
        fp16=False
    )

    return result["text"].strip()


def transcribe_all(chunks: list, language: str = "english") -> str:
    transcripts = []

    for i, chunk_path in enumerate(chunks, start=1):
        print(f"Transcribing chunk {i}/{len(chunks)}...")

        text = transcribe_chunk_whisper(chunk_path)
        transcripts.append(text)

    return "\n\n".join(transcripts)
