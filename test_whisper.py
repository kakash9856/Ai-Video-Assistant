
import os
import whisper

# FFmpeg ka exact path
FFMPEG_PATH = (
    r"C:\Users\kakas\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build\bin"
)

# FFmpeg ko current Python process ke PATH mein add karo
os.environ["PATH"] = FFMPEG_PATH + os.pathsep + os.environ["PATH"]

audio_path = r"downloades\mmns33BsBcY.wav_chunk_0.wav"

print("FFmpeg exists:", os.path.exists(os.path.join(FFMPEG_PATH, "ffmpeg.exe")), flush=True)
print("Audio exists:", os.path.exists(audio_path), flush=True)

print("Loading Whisper model...", flush=True)
model = whisper.load_model("tiny")

print("Starting transcription...", flush=True)

result = model.transcribe(
    audio_path,
    fp16=False,
    verbose=True
)

print("\nSUCCESS!", flush=True)
print(result["text"], flush=True)
