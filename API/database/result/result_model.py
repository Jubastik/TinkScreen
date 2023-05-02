import sqlalchemy as sa

from database.db_session import SqlAlchemyBase


class Result(SqlAlchemyBase):
    __tablename__ = "Results"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)