import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Admin(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'admin'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)

    def __repr__(self):
        return f"<User {self.id} {self.email}>"