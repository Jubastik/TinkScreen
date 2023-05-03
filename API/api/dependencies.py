from fastapi import Depends, status

import my_err
from my_err import APIError
from schemas.user_pdc import IdType
from service.user import UserService
from settings import settings


# def verify_root_token(root_token: str):
#     if root_token != settings().ROOT_TOKEN:
#         raise APIError(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             msg="Invalid root token",
#             err_id=my_err.INVALID_ROOT_TOKEN,
#         )


def process_user_id(obj_id: int, id_type: IdType, service: UserService = Depends()):
    return service.convert_id(id_type, obj_id)
