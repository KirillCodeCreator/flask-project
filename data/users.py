from datetime import datetime

import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase
from .role import Roles


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False, server_default='')
    firstname = sa.Column(sa.String, nullable=False)
    lastname = sa.Column(sa.String, nullable=False)
    middlename = sa.Column(sa.String)
    phone = sa.Column(sa.String, nullable=False)
    birthday = sa.Column(sa.Date)
    polis = sa.Column(sa.String)
    specialization_id = sa.Column(sa.Integer, sa.ForeignKey('specialization.id'))  # id специальности для доктора
    specialization = orm.relationship("Specialization")
    role = sa.Column(sa.String, nullable=False)
    location = sa.Column(sa.String, nullable=False, default='не задано')  # адрес консультации
    modified_date = sa.Column(sa.DateTime, default=datetime.now)


    def full_name(self):
        if self.middlename:
            return f"{self.lastname} {self.firstname} {self.middlename}"
        return f"{self.lastname} {self.firstname}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_title(self):
        if self.role == Roles.DOCTOR:
            return 'Доктор'
        elif self.role == Roles.PATIENT:
            return 'Пациент'
        elif self.role == Roles.ADMIN:
            return 'Администратор'
        else:
            return ""


    def is_admin(self):
        return self.role == Roles.ADMIN

    def is_doctor(self):
        return self.role == Roles.DOCTOR

    def is_patient(self):
        return self.role == Roles.PATIENT

    def __repr__(self):
        return f"{self.full_name()}>"
