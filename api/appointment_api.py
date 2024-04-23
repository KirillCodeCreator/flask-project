from datetime import datetime

from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import and_, or_

from api.appointmentmessages import AppointmentMessages
from api.appointmentrequired import AppointmentRequiredFields
from api.usermessages import UserMessages
from data import db_session
from data.appointment import Appointment
from data.role import Roles
from data.timeinterval import TimeInterval
from data.users import User

appointment_api = Blueprint("appointment_api", __name__, template_folder="templates")


@appointment_api.route("/api/appointments")
def get_appointments():
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).order_by(Appointment.date).order_by(
        Appointment.timeinterval_id).all()
    return jsonify(
        {"appointments": [appointment.to_dict() for appointment in appointments]}
    )


@appointment_api.route("/api/appointments/<int:appointment_id>")
def get_appointment(appointment_id):
    db_sess = db_session.create_session()
    appointment: Appointment = db_sess.get(Appointment, appointment_id)
    if not appointment:
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknown()}), 404)
    return jsonify(
        {"appointments": [appointment.to_dict()]}
    )


@appointment_api.route("/api/appointments", methods=["POST"])
def create_new_appointment():
    required_fields = AppointmentRequiredFields().required_fields()
    request_json_data = request.json
    if not request_json_data or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': AppointmentMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    doctor_id = request_json_data["doctor_id"]
    # проверяем наличие пользователя с id и ролью Доктор
    if not db_sess.query(User).filter(and_(User.id == doctor_id, User.role == Roles.DOCTOR)).first():
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 400)

    timeinterval_id = request_json_data["timeinterval_id"]
    if not db_sess.query(TimeInterval).filter(TimeInterval.id == timeinterval_id).first():
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknownDateTime()}), 400)

    date = datetime.fromisoformat(request_json_data["date"]).date()
    if date < datetime.now().date():
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknownDateTime()}), 400)

    # с использование оператора and_ ищем нет ли такой записи у доктора в эту же дату и интервал времени
    if db_sess.query(Appointment).filter(
            and_(doctor_id == Appointment.doctor_id, Appointment.timeinterval_id == timeinterval_id,
                 Appointment.date == date)).first():
        return make_response(jsonify({'message': AppointmentMessages().AppointmentExists()}), 400)

    appointment = Appointment(
        doctor_id=doctor_id,
        date=date,
        timeinterval_id=timeinterval_id,
        modified_date=datetime.now()
    )

    db_sess.add(appointment)
    db_sess.commit()
    return jsonify({'message': AppointmentMessages().AppointmentCreated()})


@appointment_api.route("/api/appointments/<int:appointment_id>", methods=["PUT"])
def update(appointment_id):
    required_fields = AppointmentRequiredFields().required_fields()
    request_json_data = request.json
    if not request_json_data or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': AppointmentMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    appointment = db_sess.get(Appointment, appointment_id)
    if not appointment:
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknown()}), 404)

    doctor_id = request_json_data["doctor_id"]
    # проверяем наличие пользователя с id и ролью Доктор
    if not db_sess.query(User).filter(and_(User.id == doctor_id, User.role == Roles.DOCTOR)).first():
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 400)

    timeinterval_id = request_json_data["timeinterval_id"]
    if not db_sess.query(TimeInterval).filter(TimeInterval.id == timeinterval_id).first():
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknownDateTime()}), 400)

    date = datetime.fromisoformat(request_json_data["date"]).date()
    if date < datetime.now().date():
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknownDateTime()}), 400)

    # с использование оператора and_ ищем нет ли такой записи у доктора в эту же дату и интервал времени
    if db_sess.query(Appointment).filter(
            and_(doctor_id == Appointment.doctor_id, Appointment.timeinterval_id == timeinterval_id,
                 Appointment.date == date)).first():
        return make_response(jsonify({'message': AppointmentMessages().AppointmentExists()}), 400)

    appointment.timeinterval_id = timeinterval_id
    appointment.date = date
    appointment.doctor_id = doctor_id
    appointment.modified_date = datetime.now()
    db_sess.commit()
    return jsonify({'message': AppointmentMessages().AppointmentUpdated()})


@appointment_api.route("/api/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    db_sess = db_session.create_session()
    appointment = db_sess.get(Appointment, appointment_id)
    if not appointment:
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknown()}), 404)
    db_sess.delete(appointment)
    db_sess.commit()
    return jsonify({'message': AppointmentMessages().AppointmentDeleted()})
