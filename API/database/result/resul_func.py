import sqlalchemy as sa
import sqlalchemy.orm as so

import my_err
from database.result.result_model import Result, ViolationType
from schemas.result_pdc import ResultCreate


class ResultF(Result):
    @classmethod
    def create_result(cls, session: so.Session, data: ResultCreate) -> (Result, int | None):
        result = ResultF(**data.dict(exclude_unset=True))
        session.add_all([result])
        session.commit()
        return result, None


class ViolationTypeF(ViolationType):
    @classmethod
    def get_by_name(cls, session: so.Session, name: str) -> (ViolationType, int | None):
        violation_type = session.scalars(sa.select(cls).where(cls.name == name)).first()
        if violation_type is None:
            return violation_type, my_err.VIOL_TYPE_NOT_FOUND
        return violation_type, None
