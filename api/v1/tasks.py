from typing import TypedDict

from fastapi import APIRouter

from schemas import TaskIn


class Task(TypedDict):
    id: int
    title: str
    status: int

tasks: list[Task] = []

    
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