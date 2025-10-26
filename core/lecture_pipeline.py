from services.transcription import transcribe_audio
from services.llm import generate_lecture_summary
from services.audio_splitter import split_audio_by_duration
from storage.json_storage import save
from utils.file_manager import cleanup
import shutil
from pathlib import Path

def run_lecture_pipeline(user_id: str, audio_file_path: str) -> list[dict]:
    """
    Пайплайн для длинных аудио:
    - разбивает аудио на чанки (~15 мин)
    - транскрибирует каждый
    - отправляет в LLM
    - возвращает список JSON-объектов с результатами
    """
    original_path = Path(audio_file_path)
    task_data = {
        "user_id": user_id,
        "original_file": str(original_path),
        "status": "pending",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "chunks": []
    }

    chunks_dir = None
    try:
        # Шаг 1: Разбить аудио
        print("→ Разбиваем аудио на чанки...")
        chunk_paths = split_audio_by_duration(audio_file_path, chunk_duration_sec=900)
        chunks_dir = Path(chunk_paths[0]).parent if chunk_paths else None

        # Шаг 2: Обработать каждый чанк
        results = []
        for i, chunk_path in enumerate(chunk_paths):
            print(f"→ Обработка чанка {i+1}/{len(chunk_paths)}...")
            raw_text = transcribe_audio(chunk_path)
            if not raw_text.strip():
                summary = "[Пустой фрагмент]"
            else:
                summary = generate_lecture_summary(raw_text)

            chunk_result = {
                "chunk_index": i,
                "audio_path": chunk_path,
                "raw_transcript": raw_text,
                "summary": summary
            }
            results.append(chunk_result)
            task_data["chunks"].append(chunk_result)

        task_data["status"] = "success"
        task_id = save(task_data)
        print(f"Задача {task_id} завершена для пользователя {user_id}")
        return results

    except Exception as e:
        task_data["status"] = "error"
        task_data["error"] = str(e)
        save(task_data)
        raise e

    finally:
        # Удаляем исходный файл И чанки
        cleanup(audio_file_path)
        if chunks_dir and chunks_dir.exists():
            shutil.rmtree(chunks_dir, ignore_errors=True)