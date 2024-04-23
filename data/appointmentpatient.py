from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase

# класс для таблицы записей пациентов на консультации
class AppointmentPatient(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "appointmentpatient"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    appointment_id = sa.Column(sa.Integer, sa.ForeignKey('appointment.id', ondelete='CASCADE'), nullable=False)  # id консультации
    appointment = orm.relationship("Appointment", passive_deletes=True)
    patient_id = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'))  # id пациента
    patient = orm.relationship("User")
    result = sa.Column(sa.String)  # диагноз
    modified_date = sa.Column(sa.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Запись на прием {self.patient.full_name()} , {self.appointment.date} {self.appointment.timeinterval} {self.appointment.doctor.full_name()}"


class PatientAppointmentRequest(SerializerMixin):
    def __int__(self, appointment_id, patient_id):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
