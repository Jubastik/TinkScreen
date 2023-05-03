from typing import List

from fastapi import APIRouter, Depends, Response
from starlette import status

import schemas.user_pdc as shm
from api.dependencies import process_user_id
from service.user import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/", response_model=List[shm.UserReturn])
async def get_users(service: UserService = Depends()):
    """
    Получить всех пользователей
    """
    return service.get_users()


@router.get("/{obj_id}", response_model=shm.UserReturn)
async def get_user(obj_id: int = Depends(process_user_id), service: UserService = Depends()):
    """
    Получить пользователя по id
    """
    return service.get_user(obj_id)


@router.post("/", response_model=shm.UserReturn)
async def create_user(student: shm.UserCreate, service: UserService = Depends()):
    """
    Создать пользователя
    """
    return service.create_user(student)


@router.delete("/{obj_id}")
async def delete_user(obj_id: int = Depends(process_user_id), service: UserService = Depends()):
    """
    Удалить пользователя
    """
    service.delete_user(obj_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
