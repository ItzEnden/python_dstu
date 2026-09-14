from typing import TypedDict

from fastapi import APIRouter
from pydantic import BaseModel, Field


class Task(TypedDict):
    id: int
    title: str
    status: int

tasks: list[Task] = []


class TaskIn(BaseModel):
    title: str
    priority: int = Field(default=0, ge=1, le=5)

    
router = APIRouter()

@router.get("/v1/tasks")
def get_tasks() -> list[Task]:
    return tasks


@router.post("/v1/tasks", status_code=201)
def post_tasks(task: TaskIn) -> Task:
    _task: Task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "status": task.priority,
    }
    
    tasks.append(_task)

    return _task