#import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from app import db
#from data.db_session import SqlAlchemyBase


class Specialization(db.Model, SerializerMixin):
    __tablename__ = "specialization"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)