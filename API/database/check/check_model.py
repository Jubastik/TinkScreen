import sqlalchemy as sa
import sqlalchemy.orm as so

from database.base import Base
from database.result.result_model import Result


class Check(Base):
    __tablename__ = "checks"
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    user: so.Mapped["User"] = so.relationship(back_populates="checks")
    text: so.Mapped[str] = so.mapped_column(sa.Text)
    results: so.Mapped["Result"] = so.relationship(back_populates="check", cascade="all, delete-orphan")
    verified: so.Mapped[bool] = so.mapped_column(default=False)
    date: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=sa.func.now())

    def __repr__(self):
        return f"<Check> {self.id} {self.user_id} {self.text} {self.date}"


