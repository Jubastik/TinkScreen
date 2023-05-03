from pydantic import BaseModel


class ViolationTypeBase(BaseModel):
    name: str
    blocking_score: float
    moderate_score: float


class ViolationTypeCreate(ViolationTypeBase):
    pass


class ViolationTypeUpdate(ViolationTypeBase):
    name: str | None
    blocking_score: float | None
    moderate_score: float | None


class ViolationTypeReturn(ViolationTypeBase):
    id: int

    class Config:
        orm_mode = True
