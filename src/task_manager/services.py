from datetime import datetime, date
from task_manager.models import Task
from task_manager.db import get_connection, init_db
from task_manager.utils import validate_due_date
import csv
import json

init_db()


def add_task(title, priority, due_date=None):
    due_date = validate_due_date(due_date)
    created_at = datetime.utcnow().isoformat()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO tasks (title, completed, priority, due_date, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, 0, priority, due_date, created_at)
        )
        task_id = cursor.lastrowid

    return Task(task_id, title, False, priority, due_date, created_at)


def list_tasks(completed=None, priority=None, overdue=False, today=False):
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if completed is not None:
        query += " AND completed = ?"
        params.append(1 if completed == "yes" else 0)

    if priority:
    # Create a placeholder for each priority
        placeholders = ",".join(["?"] * len(priority))
        query += f" AND priority IN ({placeholders})"
    # Extend the parameters list with all priorities
        params.extend(priority)

    rows = fetch_tasks(query, params)
    tasks = [row_to_task(r) for r in rows]

    if overdue:
        tasks = [t for t in tasks if is_overdue(t)]

    if today:
        tasks = [t for t in tasks if is_due_today(t)]

    tasks.sort(key=lambda t: t.due_date or "9999-12-31")
    return tasks


def mark_done(task_id):
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?",
            (task_id,)
        )
        return cur.rowcount > 0


def delete_task(task_id):
    with get_connection() as conn:
        cur = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        return cur.rowcount > 0


def fetch_tasks(query, params):
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def row_to_task(row):
    return Task(
        id=row[0],
        title=row[1],
        completed=bool(row[2]),
        priority=row[3],
        due_date=row[4],
        created_at=row[5]
    )


def is_overdue(task):
    if not task.due_date or task.completed:
        return False
    due = datetime.strptime(task.due_date, "%Y-%m-%d").date()
    return due < date.today()


def is_due_today(task):
    if not task.due_date:
        return False
    due = datetime.strptime(task.due_date, "%Y-%m-%d").date()
    return due == date.today()

def export_tasks(tasks, file_path, file_format="json"):
    if file_format == "json":
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([t.__dict__ for t in tasks], f, indent=2)
    elif file_format == "csv":
     with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "title", "priority", "due_date", "completed"]
        )
        writer.writeheader()
        for t in tasks:
            writer.writerow({
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
                "due_date": t.due_date,
                "completed": t.completed
            })
