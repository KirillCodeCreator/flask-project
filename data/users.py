from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from flask_security import UserMixin
from sqlalchemy_serializer import SerializerMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from .association_tables import specialization_users_table, role_users_table
#from .db_session import SqlAlchemyBase

class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False, server_default='')
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    middlename = db.Column(db.String)
    phone = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date)
    polis = db.Column(db.String)
    specializations = orm.relationship("Specialization", secondary=specialization_users_table, backref="User")
    roles = orm.relationship('Role', secondary=role_users_table, backref='User')
    modified_date = db.Column(sa.DateTime, default=datetime.now)
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<User {self.id} {self.name} {self.email}>"
