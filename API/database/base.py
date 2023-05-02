import sqlalchemy.orm as so


class Base(so.DeclarativeBase):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
