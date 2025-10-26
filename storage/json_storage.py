import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "tasks.json"

DATA_DIR.mkdir(exist_ok=True)

def _read_tasks():
    if not DATA_FILE.exists():
        return []
    content = DATA_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return []
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f" Ошибка чтения {DATA_FILE}: {e}. Создаём новый файл.")
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []

def save(task: dict) -> str:
    tasks = _read_tasks()
    task_id = str(len(tasks) + 1)
    task["task_id"] = task_id
    tasks.append(task)
    json_str = json.dumps(tasks, indent=2, ensure_ascii=False)
    DATA_FILE.write_text(json_str, encoding="utf-8")
    return task_id

def get(task_id: str) -> dict | None:
    tasks = _read_tasks()
    for task in tasks:
        if task.get("task_id") == task_id:
            return task
    return None