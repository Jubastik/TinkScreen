from typing import List

from fastapi import APIRouter, Depends, Response
from starlette import status

import schemas.user_pdc as shm
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

#
# @router.get("/{obj_id}", response_model=StudentReturn)
# async def get_user(obj_id: int = Depends(process_user_id), service: StudentService = Depends()):
#     """
#     Получить ученика по id
#     """
#     return service.get_student(obj_id)
#

@router.post("/", response_model=shm.UserReturn)
async def create_user(student: shm.UserCreate, service: UserService = Depends()):
    """
    Создать пользователя
    """
    return service.create_user(student)

#
# @router.patch("/{obj_id}", response_model=StudentReturn)
# async def update_user(
#     student: StudentUpdate, obj_id: int = Depends(process_user_id), service: StudentService = Depends()
# ):
#     """
#     Обновить ученика
#     """
#     return service.update_student(obj_id, student)
#
#
# @router.delete("/{obj_id}")
# async def delete_user(obj_id: int = Depends(process_user_id), service: StudentService = Depends()):
#     """
#     Удалить ученика
#     """
#     service.delete_student(obj_id)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
