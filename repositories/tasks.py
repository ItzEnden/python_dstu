from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from models.tasks import TaskModel


class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_all_tasks(self) -> list[TaskModel]:
        statement = select(TaskModel).order_by(TaskModel.id)
        return list(self.db.scalars(statement).all())

    def create_task(self, title: str, priority: int) -> TaskModel:
        task = TaskModel(title=title, priority=priority)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task_by_id(self, task_id: int) -> TaskModel | None:
        return self.db.get(TaskModel, task_id)

    def replace_task(self, task: TaskModel, title: str, priority: int) -> TaskModel:
        task.title = title
        task.priority = priority
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(
        self,
        task: TaskModel,
        title: str | None,
        priority: int | None,
    ) -> TaskModel:
        if title is not None:
            task.title = title
        if priority is not None:
            task.priority = priority
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: TaskModel) -> None:
        self.db.delete(task)
        self.db.commit()
