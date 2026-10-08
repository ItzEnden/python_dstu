from fastapi import APIRouter, Depends, Response

from models.tasks import TaskModel
from schemas import TaskIn, TaskPatch, TaskResponse
from services.tasks import TaskService


router = APIRouter(tags=["tasks"])


@router.get("/v1/tasks", response_model=list[TaskResponse])
def get_tasks(service: TaskService = Depends()) -> list[TaskModel]:
    return service.get_all_tasks()


@router.post("/v1/tasks", status_code=201, response_model=TaskResponse)
def post_tasks(task: TaskIn, service: TaskService = Depends()) -> TaskModel:
    return service.create_task(task)


@router.get("/v1/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends()) -> TaskModel:
    return service.get_task_by_id(task_id)


@router.put("/v1/tasks/{task_id}", response_model=TaskResponse)
def replace_task(task_id: int, data: TaskIn, service: TaskService = Depends()) -> TaskModel:
    return service.replace_task(task_id, data)


@router.patch("/v1/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskPatch, service: TaskService = Depends()) -> TaskModel:
    return service.update_task(task_id, data)


@router.delete("/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends()) -> Response:
    service.delete_task(task_id)
    return Response(status_code=204)
