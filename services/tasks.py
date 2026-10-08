from fastapi import Depends, HTTPException

from repositories.tasks import TaskRepository
from schemas import Task, TaskIn, TaskPatch


class TaskService:
    def __init__(self, repo: TaskRepository = Depends()) -> None:
        self.repo = repo

    def get_all_tasks(self) -> list[Task]:
        return self.repo.get_all_tasks()

    def create_task(self, data: TaskIn) -> Task:
        return self.repo.create_task(data.title, data.priority)

    def get_task_by_id(self, task_id: int) -> Task:
        task = self.repo.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def replace_task(self, task_id: int, data: TaskIn) -> Task:
        self.get_task_by_id(task_id)
        return self.repo.replace_task(task_id, data.title, data.priority)

    def update_task(self, task_id: int, data: TaskPatch) -> Task:
        self.get_task_by_id(task_id)
        return self.repo.update_task(task_id, data.title, data.priority)

    def delete_task(self, task_id: int) -> None:
        self.get_task_by_id(task_id)
        self.repo.delete_task(task_id)
