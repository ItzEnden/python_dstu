from fastapi import APIRouter, Depends, Response

from models.users import UserModel
from schemas import CreateUserRequest, UpdateUserRequest, UserResponse
from services.users import UserService


router = APIRouter(tags=["users"])


@router.post("/v1/users", status_code=201, response_model=UserResponse)
def create_user(user: CreateUserRequest, service: UserService = Depends()) -> UserModel:
    return service.create_user(user)


@router.get("/v1/users", response_model=list[UserResponse])
def get_users(service: UserService = Depends()) -> list[UserModel]:
    return service.get_all_users()


@router.get("/v1/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends()) -> UserModel:
    return service.get_user_by_id(user_id)


@router.put("/v1/users/{user_id}", response_model=UserResponse)
def replace_user(user_id: int, data: CreateUserRequest, service: UserService = Depends()) -> UserModel:
    return service.replace_user(user_id, data)


@router.patch("/v1/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UpdateUserRequest, service: UserService = Depends()) -> UserModel:
    return service.update_user(user_id, data)


@router.delete("/v1/users/{user_id}", status_code=204)
def delete_user(user_id: int, service: UserService = Depends()) -> Response:
    service.delete_user(user_id)
    return Response(status_code=204)
