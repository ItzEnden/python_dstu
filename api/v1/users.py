from fastapi import APIRouter, Depends, HTTPException

from core.exceptions import AlreadyExistsError, NotFoundError
from models.users import UserModel
from schemas import CreateUserRequest, UpdateUserRequest, UserResponse
from services.users import UserService


router = APIRouter(tags=["users"])


@router.post("/v1/users", status_code=201, response_model=UserResponse)
def create_user(user: CreateUserRequest, service: UserService = Depends()) -> UserModel:
    try:
        return service.create_user(user)
    except AlreadyExistsError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/v1/users", response_model=list[UserResponse])
def get_users(service: UserService = Depends()) -> list[UserModel]:
    return service.get_all_users()


@router.get("/v1/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends()) -> UserModel:
    try:
        return service.get_user_by_id(user_id)
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.put("/v1/users/{user_id}", response_model=UserResponse)
def replace_user(user_id: int, data: CreateUserRequest, service: UserService = Depends()) -> UserModel:
    try:
        return service.replace_user(user_id, data)
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except AlreadyExistsError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.patch("/v1/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UpdateUserRequest, service: UserService = Depends()) -> UserModel:
    try:
        return service.update_user(user_id, data)
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except AlreadyExistsError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.delete("/v1/users/{user_id}", status_code=204)
def delete_user(user_id: int, service: UserService = Depends()) -> None:
    try:
        service.delete_user(user_id)
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
