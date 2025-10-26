import tempfile
import os

def create_temp_file_with_suffix(suffix: str = ".ogg") -> str:
    """Создаёт временный файл с заданным расширением."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return path

def cleanup(path: str):
    """Безопасное удаление файла."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Не удалось удалить файл {path}: {e}")