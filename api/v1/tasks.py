from fastapi import APIRouter, Depends, Response

from schemas import Task, TaskIn, TaskPatch
from services.tasks import TaskService


router = APIRouter(tags=["tasks"])


@router.get("/v1/tasks")
def get_tasks(service: TaskService = Depends()) -> list[Task]:
    return service.get_all_tasks()


@router.post("/v1/tasks", status_code=201)
def post_tasks(task: TaskIn, service: TaskService = Depends()) -> Task:
    return service.create_task(task)


@router.get("/v1/tasks/{task_id}")
def get_task(task_id: int, service: TaskService = Depends()) -> Task:
    return service.get_task_by_id(task_id)


@router.put("/v1/tasks/{task_id}")
def replace_task(task_id: int, data: TaskIn, service: TaskService = Depends()) -> Task:
    return service.replace_task(task_id, data)


@router.patch("/v1/tasks/{task_id}")
def update_task(task_id: int, data: TaskPatch, service: TaskService = Depends()) -> Task:
    return service.update_task(task_id, data)


@router.delete("/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends()) -> Response:
    service.delete_task(task_id)
    return Response(status_code=204)
