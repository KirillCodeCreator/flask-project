from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from datetime import datetime
from sqlalchemy import orm
import sqlalchemy as sa

class AppointmentStatus:
    Created = "Открыт"
    SETPATIENT = "Назначен"
    Canceled = "Отменен"
    Finished = "Завершен"



# класс для таблицы консультаций
class Appointment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "appointment"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    startdate = sa.Column(sa.Date, default=datetime.now(), nullable=False) #дата начала консультации
    enddate = sa.Column(sa.Date, nullable=False) #дата и время окончания консультации
    doctor_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False) # id доктора
    doctor = orm.relationship("User")
    patient_id = sa.Column(sa.Integer, sa.ForeignKey('user.id')) # id пациента
    patient = orm.relationship("User")
    location = sa.Column(sa.String, nullable=False) #адрес консультации
    status = sa.Column(sa.String, nullable=False, default=AppointmentStatus().Created)
    result = sa.Column(sa.Text)  # описание результата, диагноз

    def __repr__(self):
        return f"<Jobs {self.id} {self.startdate} {self.enddate} {self.location} {self.doctor} {self.patient}>"