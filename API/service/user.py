from fastapi import Depends, status
from sqlalchemy.orm import Session

import my_err
from database.db_session import get_session
import schemas.user_pdc as shm
from database.user.user_func import UserF
from database.user.user_model import User


class UserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def convert_id(self, id_type: shm.IdType, obj_id: int) -> int:
        if id_type == shm.IdType.telegram:
            user, err = UserF.get_user_by_tg_id(self.session, obj_id)
        elif id_type == shm.IdType.database:
            user, err = UserF.get_user(self.session, obj_id)
        else:
            raise my_err.APIError(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                my_err.IN_DEVELOPMENT,
                "Неверный тип id",
            )
        if err is not None:
            raise my_err.APIError(status.HTTP_404_NOT_FOUND, err)
        return user.id

    def get_users(self) -> list[shm.UserReturn]:
        users, err = UserF.get_users(self.session)
        return users

    def get_user(self, dbid) -> shm.UserReturn:
        user, err = UserF.get_user(self.session, dbid)
        if err is not None:
            raise my_err.APIError(status.HTTP_404_NOT_FOUND, err)
        return user

    def create_user(self, data_user: shm.UserCreate) -> User:
        user, err = UserF.create_user(self.session, data_user)
        if err is not None:
            raise my_err.APIError(
                status_code=status.HTTP_400_BAD_REQUEST,
                err_id=err,
            )
        return user

    def delete_user(self, user_id: int):
        err = UserF.delete_user(self.session, user_id)
        if err is not None:
            raise my_err.APIError(404, err)
