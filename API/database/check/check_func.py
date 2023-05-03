from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas import check_pdc as shm

from . import check_model


class CheckF(check_model.Check):
    @classmethod
    def create_check(cls, session: Session, data_check: shm.CheckCreate) -> (check_model.Check, int | None):
        data = data_check.dict(exclude_unset=True)
        if "tg_id" in data:
            del data["tg_id"]
        check = CheckF(**data)
        session.add_all([check])
        session.commit()
        return check, None

    @classmethod
    def get_checks(cls, session: Session) -> (list[check_model.Check], int | None):
        checks = session.scalars(select(cls)).all()
        return checks, None

    @classmethod
    def get_my_checks(cls, session: Session, user_id: int) -> (list[check_model.Check], int | None):
        checks = session.scalars(select(cls).where(cls.user_id == user_id)).all()
        return checks, None
