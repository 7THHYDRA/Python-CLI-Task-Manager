from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
