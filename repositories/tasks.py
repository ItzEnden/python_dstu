from schemas import Task


_tasks: dict[int, Task] = {}


class TaskRepository:
    def get_all_tasks(self) -> list[Task]:
        return list(_tasks.values())

    def create_task(self, title: str, priority: int) -> Task:
        task_id = max(_tasks, default=0) + 1
        task: Task = {
            "id": task_id,
            "title": title,
            "priority": priority,
        }
        _tasks[task_id] = task
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return _tasks.get(task_id)

    def replace_task(self, task_id: int, title: str, priority: int) -> Task:
        task = _tasks[task_id]
        task["title"] = title
        task["priority"] = priority
        return task

    def update_task(self, task_id: int, title: str | None, priority: int | None) -> Task:
        task = _tasks[task_id]
        if title is not None:
            task["title"] = title
        if priority is not None:
            task["priority"] = priority
        return task

    def delete_task(self, task_id: int) -> None:
        del _tasks[task_id]
