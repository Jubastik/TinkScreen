import sqlalchemy as sa
import sqlalchemy.orm as so

from database.base import Base


class Check(Base):
    __tablename__ = "checks"
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    user: so.Mapped["User"] = so.relationship(back_populates="checks")
    text: so.Mapped[str] = so.mapped_column(sa.Text)
    date: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=sa.func.now())

    def __repr__(self):
        return f"<Check> {self.id} {self.user_id} {self.text} {self.date}"


