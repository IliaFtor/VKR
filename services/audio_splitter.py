import os
import subprocess
from pathlib import Path

def split_audio_by_duration(input_path: str, chunk_duration_sec: int = 900) -> list[str]:
    """
    Разбивает аудиофайл на чанки по chunk_duration_sec секунд (по умолчанию 15 мин = 900 сек).
    Возвращает список путей к чанкам.
    """
    input_path = Path(input_path)
    output_dir = input_path.parent / f"{input_path.stem}_chunks"
    output_dir.mkdir(exist_ok=True)

    # Команда ffmpeg: разбить на чанки без перекодирования
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-f", "segment",
        "-segment_time", str(chunk_duration_sec),
        "-c", "copy",
        str(output_dir / f"{input_path.stem}_part%03d.ogg")
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunks = sorted(output_dir.glob("*.ogg"))
        return [str(p) for p in chunks]
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ошибка разбиения аудио: {e}")