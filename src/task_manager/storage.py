import json
from pathlib import Path
from task_manager.models import Task

DATA_FILE = Path("data/tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Task(**item) for item in data]


def save_tasks(tasks):
    DATA_FILE.parent.mkdir(exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [task.__dict__ for task in tasks],
            f,
            indent=2
        )
