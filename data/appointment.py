from sqlalchemy_serializer import SerializerMixin

from app import db
#from data.db_session import SqlAlchemyBase
from datetime import datetime
from sqlalchemy import orm
import sqlalchemy as sa

# класс для таблицы консультаций
class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startdate = db.Column(db.DateTime, default=datetime.now(), nullable=False) #дата начала консультации
    enddate = db.Column(db.DateTime, nullable=False) #дата и время окончания  консультации
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # id доктора
    doctor = orm.relationship("User")
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id')) # id пациента
    patient = orm.relationship("User")
    location = db.Column(db.String, nullable=False) #адрес консультации
    is_finished = db.Column(db.Boolean, default=False)
    result = db.Column(db.Text)  # описание результата, диагноз

    def __repr__(self):
        return f"<Jobs {self.id} {self.doctor} {self.date} {self.time} {self.location}>"