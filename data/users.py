from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .association_tables import specialization_users_table, role_users_table
from .db_session import SqlAlchemyBase

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
    specializations = orm.relationship("Specialization", secondary=specialization_users_table, backref="User")
    roles = orm.relationship('Role', secondary=role_users_table, backref='User')
    modified_date = sa.Column(sa.DateTime, default=datetime.now)
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<User {self.id} {self.name} {self.email}>"
