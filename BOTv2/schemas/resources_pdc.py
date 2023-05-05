from enum import Enum

from pydantic import BaseModel, UUID4

from schemas.broker_pdc import Status


class Resource(BaseModel):
    name: str
    status: Status
    rating: float | None
    uuid: UUID4
