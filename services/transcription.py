import whisper
from pathlib import Path

_model = None

def get_whisper_model():
    global _model
    if _model is None:
        print("Загружаем Whisper (base)...")
        _model = whisper.load_model("base")
    return _model

def transcribe_audio(file_path: str) -> str:
    """Транскрибирует аудио в текст."""
    model = get_whisper_model()
    result = model.transcribe(file_path, language="ru", fp16=False)
    return result["text"].strip()