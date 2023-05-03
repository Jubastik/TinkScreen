from fastapi import Depends, status
from sqlalchemy.orm import Session

from database.db_session import get_session
import schemas.user_pdc as shm
from database.user.user_model import User


class UserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_users(self) -> list[shm.UserReturn]:
        pass
        return

    def create_user(self, data_user: shm.UserCreate) -> User:
        user = User(**data_user.dict(exclude_unset=True))
        self.session.add_all([user])
        self.session.commit()
        return user
