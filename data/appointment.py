from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Mapped
from sqlalchemy_serializer import SerializerMixin

from data.appointmentpatient import AppointmentPatient
from data.db_session import SqlAlchemyBase


class AppointmentStatus:
    Created = "Открыт"
    Canceled = "Отменен"
    Finished = "Завершен"


# класс для таблицы консультаций
class Appointment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "appointment"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date = sa.Column(sa.Date, nullable=False, default=datetime.today())  # дата консультации
    timeinterval_id = sa.Column(sa.Integer, sa.ForeignKey('timeinterval.id'), nullable=False)  # время консультации
    timeinterval = orm.relationship("TimeInterval")
    doctor_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)  # id доктора
    doctor = orm.relationship("User")
    modified_date = sa.Column(sa.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Прием {self.doctor.specialization} {self.doctor}, {self.date}, {self.timeinterval}, {self.location}"
