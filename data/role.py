import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from flask_login import RoleMixin
from data.db_session import SqlAlchemyBase

class Roles:
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    PATIENT = "PATIENT"

class Role(SqlAlchemyBase, RoleMixin, SerializerMixin):
    __tablename__ = 'role'
    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(80), unique=True)