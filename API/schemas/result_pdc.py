from pydantic import BaseModel

from schemas.violation_type_pdc import ViolationTypeReturn


class ResultBase(BaseModel):
    score: float
    is_violation: bool
    violation: str
    type_id: int
    check_id: int


class ResultCreate(ResultBase):
    pass


class ResultUpdate(ResultBase):
    score: float | None
    is_violation: bool | None
    violation: str | None
    type_id: int | None
    check_id: int | None


class ResultReturn(ResultBase):
    id: int
    type: ViolationTypeReturn

    class Config:
        orm_mode = True
