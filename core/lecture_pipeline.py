from services.transcription import transcribe_audio
from services.llm import generate_lecture_summary
from storage.json_storage import save
from utils.file_manager import cleanup

def run_lecture_pipeline(user_id: str, audio_file_path: str) -> str:
    """
    Основной пайплайн: аудио → транскрипция → конспект → сохранение в хранилище.
    Возвращает готовый конспект.
    """
    task_data = {
        "user_id": user_id,
        "input_file_path": audio_file_path,
        "status": "pending",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }

    try:
        # Шаг 1: Транскрипция
        raw_text = transcribe_audio(audio_file_path)
        task_data["raw_transcript"] = raw_text
        if not raw_text.strip():
            raise ValueError("Не удалось распознать речь")

        # Шаг 2: Генерация конспекта
        summary = generate_lecture_summary(raw_text)
        task_data["summary"] = summary
        task_data["status"] = "success"

        # Шаг 3: Сохранение в хранилище
        task_id = save(task_data)

        print(f"Задача {task_id} завершена для пользователя {user_id}")
        return summary

    except Exception as e:
        task_data["status"] = "error"
        task_data["error"] = str(e)
        save(task_data)
        raise e

    finally:
        # Удаляем временный файл
        cleanup(audio_file_path)