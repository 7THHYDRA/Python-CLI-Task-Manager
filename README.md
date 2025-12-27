<!-- @format -->

# Task Manager CLI

**Task Manager CLI** is a lightweight, Python-based command-line application for managing tasks. It supports multiple priorities, due dates, task completion, and exporting tasks to CSV or JSON. Built with **SQLite** for persistent storage, this project is ideal for personal productivity and small-scale task tracking.

---

## Features

- Add tasks with **priority** and **due dates**
- List tasks with filters:
  - By **completed status** (`--completed yes|no`)
  - By **priority** (`--priority high medium`)
  - By **overdue** (`--overdue`)
  - By **today** (`--today`)
- Mark tasks as done (`done <id>`)
- Delete tasks (`delete <id>`)
- Export tasks to **JSON** or **CSV** (`export --format csv --output file.csv`)
- SQLite backend for persistent storage

---

## Installation

### Using pip (after packaging):

```bash
pip install .


#task execution

#add task
task add "Learn Python" --priority high --due 2025-01-10

#list task
task list

#Filter task by priority
task list --priority high medium

#list overdue task
task list --overdue

#list tasks due today
task list --today

#Mark a task as done
task done 1

#delete a task
task delete 2

# Export as CSV
task export --format csv --output my_tasks.csv

# Export as JSON
task export --format json --output my_tasks.json

#Run test using unittest
python -m unittest discover tests



```

## License

This project is licensed under the [MIT License](LICENSE) – see the LICENSE file for details.

## Acknowledgements

- Python standard libraries: `argparse`, `csv`, `json`, `sqlite3`, `datetime`
- Inspired by personal productivity workflows and CLI applications
- Thanks to contributors and testers for feedback
