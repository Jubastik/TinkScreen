from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from database.base import Base


class User(Base):
    __tablename__ = "users"
    name: so.Mapped[str] = so.mapped_column(sa.String(30))
    tg_id: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger, unique=True)
    checks: so.Mapped[List["Check"]] = so.relationship(back_populates="creator", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User> {self.id} {self.name} {self.tg_id}"
