from fastapi import Depends, status
from sqlalchemy.orm import Session

import my_err
from database.check.check_func import CheckF
from database.check.check_model import Check
from database.db_session import get_session
import schemas.check_pdc as shm
import schemas.result_pdc as res_shm
from database.result.resul_func import ViolationTypeF, ResultF
from database.user.user_func import UserF


class CheckService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_check(self, data_check: shm.CheckCreate) -> Check:
        if data_check.user_id is None and data_check.tg_id:
            user, err = UserF.get_user_by_tg_id(self.session, data_check.tg_id)
            if err is not None:
                raise my_err.APIError(status.HTTP_404_NOT_FOUND, err)
            data_check.user_id = user.id
        check, err = CheckF.create_check(self.session, data_check)
        if err is not None:
            pass
        scores = {
            "manipulation": 0,
            "profanity": 0,
            "advertisement": 0,
            "begging": 0,
        }
        for type, score in scores.items():
            db_type, err = ViolationTypeF.get_by_name(self.session, type)
            if err is not None:
                raise my_err.APIError(status.HTTP_404_NOT_FOUND, err)
            is_violation = True if score >= db_type.block_score else False
            result, err = ResultF.create_result(self.session, res_shm.ResultCreate(score=score,
                                                                                   is_violation=is_violation,
                                                                                   violation="",
                                                                                   type_id=db_type.id,
                                                                                   check_id=check.id))

        return check

    def get_checks(self) -> list[Check]:
        checks, err = CheckF.get_checks(self.session)
        return checks

    def get_my_checks(self, user_id: int) -> list[Check]:
        checks, err = CheckF.get_my_checks(self.session, user_id)
        return checks
