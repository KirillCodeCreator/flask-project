from datetime import datetime

from flask import Blueprint, jsonify, request, make_response

from api.usermessages import UserMessages
from api.userrequired import UserRequiredFields
from data import db_session
from data.appointment import Appointment
from data.appointmentpatient import AppointmentPatient
from data.role import Roles
from data.specialization import Specialization
from data.users import User

doctor_api = Blueprint("doctor_api", __name__, template_folder="templates")


@doctor_api.route("/api/doctors")
def get_doctors():
    db_sess = db_session.create_session()
    doctors = db_sess.query(User).filter(User.role == Roles().DOCTOR).order_by(User.lastname.desc()).all()
    return jsonify(
        {"doctors": [doctor.to_dict() for doctor in doctors]}
    )


@doctor_api.route("/api/doctors/appointmentpatients/<int:doctor_id>")
def get_doctor_appointments(doctor_id):
    db_sess = db_session.create_session()

    appointments = (db_sess.query(Appointment).filter(Appointment.doctor_id == doctor_id).all())

    result = []
    for ap in appointments:
        appointmentPatients = db_sess.query(AppointmentPatient).filter(AppointmentPatient.appointment_id == ap.id).all()
        if appointmentPatients:
            for p in appointmentPatients:
                r = {"id": ap.id, "date": ap.date.strftime("%Y-%m-%d"),
                     "time": ap.timeinterval.starttime.strftime("%H:%M"), "patient": p.patient.full_name(),
                     "result": p.result}
                result.append(r)
        else:
            r = {"id": ap.id, "date": ap.date.strftime("%Y-%m-%d"), "time": ap.timeinterval.starttime.strftime("%H:%M")}
            result.append(r)

    return jsonify(
        {"appointments": [item for item in result]}
    )


@doctor_api.route("/api/doctors/<int:doctor_id>")
def get_doctor(doctor_id):
    db_sess = db_session.create_session()
    doctor: User = db_sess.get(User, doctor_id)
    if not doctor or doctor.role != Roles().DOCTOR:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 404)
    return jsonify(
        {"doctors": [doctor.to_dict()]}
    )


@doctor_api.route("/api/doctors", methods=["POST"])
def create_doctor():
    required_fields = UserRequiredFields().doctor_created_required_fields()
    if not request.json or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': UserMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    spec = db_sess.get(Specialization, int(request.json["specialization_id"]))
    if not spec:
        return make_response(jsonify({'message': UserMessages().UserUnknownSpec()}), 400)

    password_hash = request.json["hashed_password"]
    hash_method = password_hash.split("$")[0]
    if ":".join(hash_method.split(':')[:2]) == "pbkdf2:sha256":
        return make_response(jsonify({'message': UserMessages().UserWrongHashPassword()}), 400)

    doctor = User(
        firstname=request.json["firstname"],
        lastname=request.json["lastname"],
        middlename=request.json["middlename"],
        birthday=datetime.strptime(request.json["birthday"], '%Y-%m-%d').date(),
        phone=request.json["phone"],
        specialization_id=request.json["specialization_id"],
        role=Roles.DOCTOR,
        email=request.json["email"],
        hashed_password=password_hash,
        location=request.json["location"],
        modified_date=datetime.now(),
    )
    if db_sess.query(User).filter(User.email == doctor.email).first():
        return make_response(jsonify({'message': UserMessages().UserEmailExists()}), 400)
    db_sess.add(doctor)
    db_sess.commit()
    return jsonify({'message': UserMessages().UserRegistered(doctor)})


@doctor_api.route("/api/doctors/<int:doctor_id>", methods=["PUT"])
def edit_doctor(doctor_id):
    required_fields = UserRequiredFields().doctor_update_required_fields()
    if not request.json or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': UserMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    spec = db_sess.get(Specialization, int(request.json["specialization_id"]))
    if not spec:
        return make_response(jsonify({'message': UserMessages().UserUnknownSpec()}), 400)

    doctor = db_sess.get(User, doctor_id)
    if not doctor:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 404)
    if doctor.role != Roles.DOCTOR:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 400)

    password_hash = request.json["hashed_password"]
    hash_method = password_hash.split("$")[0]
    if ":".join(hash_method.split(':')[:2]) == "pbkdf2:sha256":
        return make_response(jsonify({'message': UserMessages().UserWrongHashPassword()}), 400)

    birthday = datetime.strptime(request.json["birthday"], '%d/%m/%Y').date()
    doctor.firstname = request.json["firstname"]
    doctor.lastname = request.json["lastname"]
    doctor.middlename = request.json["middlename"]
    doctor.birthday = birthday
    doctor.phone = request.json["phone"]
    doctor.specialization_id = request.json["specialization_id"]
    doctor.hashed_password = password_hash
    doctor.location = request.json["location"]
    doctor.modified_date = datetime.now()
    db_sess.commit()
    return jsonify({'message': UserMessages().UserRegistered(doctor)})


@doctor_api.route("/api/doctors/<int:doctor_id>", methods=["DELETE"])
def delete_doctor(doctor_id):
    db_sess = db_session.create_session()
    doctor = db_sess.get(User, doctor_id)
    if not doctor or doctor.role != Roles.DOCTOR:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 404)
    db_sess.delete(doctor)
    db_sess.commit()
    return jsonify({'message': UserMessages().UserDeleted(doctor)})
