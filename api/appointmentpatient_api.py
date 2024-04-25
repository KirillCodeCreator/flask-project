from datetime import datetime

from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import and_

from api.appointmentmessages import AppointmentMessages
from api.appointmentpatientsrequired import AppointmentPatientsRequiredFields
from api.usermessages import UserMessages
from data import db_session
from data.appointment import Appointment
from data.appointmentpatient import AppointmentPatient
from data.role import Roles
from data.users import User

appointmentpatient_api = Blueprint("appointmentpatient_api", __name__, template_folder="templates")


@appointmentpatient_api.route("/api/appointmentpatients")
def get_appointments():
    db_sess = db_session.create_session()
    appointmentpatients = db_sess.query(AppointmentPatient).all()
    return jsonify(
        {"appointmentpatients": [appointmentpatient.to_dict() for appointmentpatient in appointmentpatients]}
    )


@appointmentpatient_api.route("/api/appointmentpatients/patient/<int:patient_id>")
def get_patient_appointments(patient_id):
    db_sess = db_session.create_session()
    appointmentpatients = db_sess.query(AppointmentPatient).filter(AppointmentPatient.patient_id == patient_id).all()
    return jsonify(
        {"appointmentpatients": [appointmentpatient.to_dict() for appointmentpatient in appointmentpatients]}
    )


@appointmentpatient_api.route("/api/appointmentpatients/<int:appointmentpatient_id>")
def get_appointment(appointmentpatient_id):
    db_sess = db_session.create_session()
    appointmentpatient: Appointment = db_sess.get(AppointmentPatient, appointmentpatient_id)
    if not appointmentpatient:
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknown()}), 404)
    return jsonify(
        {"appointmentpatients": [appointmentpatient.to_dict()]}
    )


@appointmentpatient_api.route("/api/appointmentpatients", methods=["POST"])
def create():
    required_fields = AppointmentPatientsRequiredFields().create_required_fields()
    request_json_data = request.json
    if not request_json_data or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': AppointmentMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    patient_id = int(request_json_data["patient_id"])
    # проверяем наличие пользователя с id и ролью пациент
    if not db_sess.query(User).filter(and_(User.id == patient_id, User.role == Roles.PATIENT)).first():
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 400)

    # проверяем наличие такой записи
    appointment_id = int(request_json_data["appointment_id"])
    if not db_sess.query(Appointment).filter(Appointment.id == appointment_id).first():
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknown()}), 400)

    appointmentpatient = AppointmentPatient(
        appointment_id=appointment_id,
        patient_id=patient_id,
        modified_date=datetime.now()
    )

    try:
        db_sess.add(appointmentpatient)
        db_sess.commit()
        return jsonify({'message': AppointmentMessages().AppointmentCreated()})
    except Exception as e:
        return jsonify({'message': AppointmentMessages().AppointmentExists()})


@appointmentpatient_api.route("/api/appointmentpatients/<int:appointmentpatient_id>", methods=["PUT"])
def update_appointment(appointmentpatient_id):
    required_fields = AppointmentPatientsRequiredFields().update_required_fields()
    request_json_data = request.json
    if not request_json_data or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': AppointmentMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    appointment = db_sess.get(AppointmentPatient, appointmentpatient_id)
    if not appointment:
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknown()}), 404)

    result = request_json_data["result"]
    appointment.result = result
    appointment.modified_date = datetime.now()
    db_sess.commit()
    return jsonify({'message': AppointmentMessages().AppointmentUpdated()})


@appointmentpatient_api.route("/api/appointmentpatients/<int:appointmentpatient_id>", methods=["DELETE"])
def delete_appointment(appointmentpatient_id):
    db_sess = db_session.create_session()
    appointment = db_sess.get(AppointmentPatient, appointmentpatient_id)
    if not appointment:
        return make_response(jsonify({'message': AppointmentMessages().AppointmentUnknown()}), 404)
    db_sess.delete(appointment)
    db_sess.commit()
    return jsonify({'message': AppointmentMessages().AppointmentDeleted()})
