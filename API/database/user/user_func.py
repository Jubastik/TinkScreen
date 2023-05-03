from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import my_err
from . import user_model
from schemas import user_pdc as shm


class UserF(user_model.User):
    @classmethod
    def get_user(cls, session: Session, user_id: int) -> (user_model.User, int | None):
        user = session.scalars(select(cls).where(cls.id == user_id)).first()
        if user is None:
            return user, my_err.USER_NOT_FOUND

        return user, None

    @classmethod
    def create_user(cls, session: Session, data_user: shm.UserCreate) -> (user_model.User, int | None):
        user = UserF(**data_user.dict(exclude_unset=True))
        try:
            session.add_all([user])
            session.commit()
        except IntegrityError as e:
            return user, my_err.TG_ID_OCCUPIED
        return user, None

    @classmethod
    def get_users(cls, session: Session) -> (user_model.User, int | None):
        users = session.scalars(select(cls)).all()
        return users, None

    @classmethod
    def get_user_by_tg_id(cls, session: Session, tg_id: int) -> (user_model.User, int | None):
        user = session.scalars(select(cls).where(cls.tg_id == tg_id)).first()
        if user is None:
            return user, my_err.USER_NOT_FOUND
        return user, None

    @classmethod
    def delete_user(cls, session: Session, user_id: int) -> int | None:
        user, err = UserF.get_user(session, user_id)
        if err is not None:
            return err
        session.delete(user)
        session.commit()
        return None
