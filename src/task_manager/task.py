import argparse
from task_manager.services import (
    add_task,
    list_tasks,
    mark_done,
    delete_task
)


def main():
    parser = argparse.ArgumentParser(
        description="Python CLI Task Manager (SQLite)"
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    add_parser.add_argument("--priority",
                            nargs="+",
                            choices=["high", "medium", "low"],
                            )
    add_parser.add_argument("--due")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--completed",
                             choices=["yes", "no"])
    list_parser.add_argument("--priority",
                             nargs="+",
                             choices=["high", "medium", "low"],
                             help="Filter by one or more priorities")
    list_parser.add_argument("--overdue",
                             action="store_true")
    list_parser.add_argument("--today",
                             action="store_true")

    done_parser = subparsers.add_parser("done")
    done_parser.add_argument("id", type=int)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)


    export_parser = subparsers.add_parser(
    "export",
    help="Export tasks to JSON or CSV"
)
    export_parser.add_argument(
        "--format",
          choices=["json", "csv"],
          default="json",
          help="Output format"
)
    export_parser.add_argument(
      "--output",
      help="Output file name (default: tasks_export.{format})"
)


    args = parser.parse_args()

    if args.command == "add":
        try:
            task = add_task(
                args.title,
                args.priority,
                args.due
            )
            print(f"Added task #{task.id}")
        except ValueError as e:
            print(e)

    elif args.command == "list":
        tasks = list_tasks(
            completed=args.completed,
            priority=args.priority,
            overdue=args.overdue,
            today=args.today
        )

        if not tasks:
            print("No tasks found.")
            return

        for t in tasks:
            status = "✓" if t.completed else " "
            due = t.due_date or "No due date"
            print(f"[{status}] {t.id}. {t.title} | {t.priority} | Due: {due}")

    elif args.command == "done":
        print("Task completed!" if mark_done(args.id)
              else "Task not found")

    elif args.command == "delete":
        print("Task deleted!" if delete_task(args.id)
              else "Task not found")
        
    elif args.command == "export":
            tasks = list_tasks()  # optionally apply filters
            output_file = args.output or f"tasks_export.{args.format}"

            from task_manager.services import export_tasks
            export_tasks(tasks, output_file, args.format)

            print(f"Tasks exported to {output_file}")


    else:
        parser.print_help()


if __name__ == "__main__":
    main()
