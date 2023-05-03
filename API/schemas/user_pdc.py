from enum import Enum

from pydantic import BaseModel


class IdType(Enum):
    telegram = "student_tg"
    database = "student_db"


class UserBase(BaseModel):
    name: str | None
    tg_id: int | None


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserReturn(UserBase):
    id: int

    class Config:
        orm_mode = True
