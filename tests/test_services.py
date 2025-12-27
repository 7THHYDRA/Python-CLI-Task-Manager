import unittest
import os
from task_manager.services import add_task, list_tasks, mark_done, delete_task
from task_manager.db import DB_PATH, init_db

class TestServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Only delete the DB if it exists
        if DB_PATH.exists():
            try:
                os.remove(DB_PATH)
            except PermissionError:
                # Windows may lock the file, ignore and just init DB
                pass
        init_db()
