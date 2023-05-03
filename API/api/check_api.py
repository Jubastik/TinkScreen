from typing import List

from fastapi import APIRouter, Depends, Response
from starlette import status

import schemas.check_pdc as shm
from api.dependencies import process_user_id
from service.check import CheckService

router = APIRouter(
    prefix="/check",
    tags=["check"],
)


@router.get("/", response_model=List[shm.CheckReturn])
async def get_checks(service: CheckService = Depends()):
    """
    Получить все проверки
    """
    return service.get_checks()


# @router.get("/{obj_id}", response_model=shm.CheckReturn)
# async def get_check(obj_id: int = Depends(process_user_id), service: CheckService = Depends()):
#     """
#     Получить проверку по id
#     """
#     return service.get_user(obj_id)


@router.get("/my/{obj_id}", response_model=list[shm.CheckReturn])
async def get_check(obj_id: int = Depends(process_user_id), service: CheckService = Depends()):
    """
    Получить проверки по пользователя
    """
    return service.get_my_checks(obj_id)


@router.post("/", response_model=shm.CheckReturn)
async def create_check(check: shm.CheckCreate, service: CheckService = Depends()):
    """
    Создать проверку
    """
    return service.create_check(check)
