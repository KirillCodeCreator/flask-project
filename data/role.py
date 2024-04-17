import sqlalchemy as sa
from flask_security import RoleMixin
from sqlalchemy_serializer import SerializerMixin

from app import db
from data.db_session import SqlAlchemyBase


class AdminRoleConfiguration:
    DefaultName = "ADMIN"


class DoctorRoleConfiguration:
    DefaultName = "DOCTOR"


class PatientRoleConfiguration:
    DefaultName = "PATIENT"


class Role(db.Model, RoleMixin, SerializerMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
