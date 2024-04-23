import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Specialization(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "specialization"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
