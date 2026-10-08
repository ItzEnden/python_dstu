from typing import TypedDict

from fastapi import APIRouter, HTTPException, Response

from schemas import TaskIn, TaskPatch


class Task(TypedDict):
    id: int
    title: str
    priority: int


tasks: list[Task] = []
router = APIRouter(tags=["tasks"])


def find_task(task_id: int) -> Task:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.get("/v1/tasks")
def get_tasks() -> list[Task]:
    return tasks


@router.post("/v1/tasks", status_code=201)
def post_tasks(task: TaskIn) -> Task:
    new_task_id = max((existing_task["id"] for existing_task in tasks), default=0) + 1
    new_task: Task = {
        "id": new_task_id,
        "title": task.title,
        "priority": task.priority,
    }
    tasks.append(new_task)
    return new_task


@router.get("/v1/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    return find_task(task_id)


@router.put("/v1/tasks/{task_id}")
def replace_task(task_id: int, data: TaskIn) -> Task:
    task = find_task(task_id)
    task["title"] = data.title
    task["priority"] = data.priority
    return task


@router.patch("/v1/tasks/{task_id}")
def update_task(task_id: int, data: TaskPatch) -> Task:
    task = find_task(task_id)
    if data.title is not None:
        task["title"] = data.title
    if data.priority is not None:
        task["priority"] = data.priority
    return task


@router.delete("/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> Response:
    tasks.remove(find_task(task_id))
    return Response(status_code=204)
