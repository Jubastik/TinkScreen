from datetime import datetime

from pydantic import BaseModel
from schemas.result_pdc import ResultReturn


class CheckBase(BaseModel):
    user_id: int | None
    text: str


class CheckCreate(CheckBase):
    tg_id: int | None


class CheckUpdate(CheckBase):
    user_id: int | None
    text: str | None
    verified: bool | None
    date: datetime | None


class CheckReturn(CheckBase):
    id: int
    results: list[ResultReturn] | None

    class Config:
        orm_mode = True
