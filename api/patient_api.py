from datetime import datetime

from flask import Blueprint, jsonify, request, make_response

from api.usermessages import UserMessages
from api.userrequired import UserRequiredFields
from data import db_session
from data.role import Roles
from data.users import User

patient_api = Blueprint("patient_api", __name__, template_folder="templates")


@patient_api.route("/api/patients")
def get_patients():
    db_sess = db_session.create_session()
    patients = db_sess.query(User).filter(User.role == Roles().PATIENT).order_by(
        User.lastname.desc()).order_by(User.firstname.desc()).all()
    return jsonify(
        {"patients": [patient.to_dict() for patient in patients]}
    )


@patient_api.route("/api/patients/<int:patient_id>")
def get_patient(patient_id):
    db_sess = db_session.create_session()
    patient: User = db_sess.get(User, patient_id)
    if not patient or patient.role != Roles().PATIENT:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 404)
    return jsonify(
        {"patients": [patient.to_dict()]}
    )


@patient_api.route("/api/patients", methods=["POST"])
def create_patient():
    required_fields = UserRequiredFields().patient_created_required_fields()
    if not request.json or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': UserMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    password_hash = request.json["hashed_password"]
    hash_method = password_hash.split("$")[0]
    if ":".join(hash_method.split(':')[:2]) == "pbkdf2:sha256":
        return make_response(jsonify({'message': UserMessages().UserWrongHashPassword()}), 400)

    patient = User(
        firstname=request.json["firstname"],
        lastname=request.json["lastname"],
        middlename=request.json["middlename"],
        birthday=datetime.strptime(request.json["birthday"], '%Y-%m-%d').date(),
        phone=request.json["phone"],
        role=Roles.PATIENT,
        polis=request.json["polis"],
        email=request.json["email"],
        hashed_password=password_hash,
        location=request.json["location"],
        modified_date=datetime.now(),
    )
    if db_sess.query(User).filter(User.email == patient.email).first():
        return make_response(jsonify({'message': UserMessages().UserEmailExists()}), 400)
    db_sess.add(patient)
    db_sess.commit()
    return jsonify({'message': UserMessages().UserRegistered(patient)})


@patient_api.route("/api/patients/<int:patient_id>", methods=["PUT"])
def edit_patient(patient_id):
    required_fields = UserRequiredFields().patient_update_required_fields()
    if not request.json or not all(key in request.json for key in required_fields):
        return make_response(jsonify({'message': UserMessages().MissingFields()}), 400)

    db_sess = db_session.create_session()
    patient = db_sess.get(User, patient_id)
    if not patient:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 404)
    if patient.role != Roles.PATIENT:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 400)

    password_hash = request.json["hashed_password"]
    hash_method = password_hash.split("$")[0]
    if ":".join(hash_method.split(':')[:2]) == "pbkdf2:sha256":
        return make_response(jsonify({'message': UserMessages().UserWrongHashPassword()}), 400)

    birthday = datetime.strptime(request.json["birthday"], '%d/%m/%Y').date()
    patient.firstname = request.json["firstname"]
    patient.lastname = request.json["lastname"]
    patient.middlename = request.json["middlename"]
    patient.birthday = birthday
    patient.phone = request.json["phone"]
    patient.polis = request.json["polis"]
    patient.hashed_password = password_hash
    patient.location = request.json["location"]
    patient.modified_date = datetime.now()
    db_sess.commit()
    return jsonify({'message': UserMessages().UserUpdated(patient)})


@patient_api.route("/api/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    db_sess = db_session.create_session()
    patient = db_sess.get(User, patient_id)
    if not patient or patient.role != Roles.PATIENT:
        return make_response(jsonify({'message': UserMessages().UserUnknown()}), 404)
    db_sess.delete(patient)
    db_sess.commit()
    return jsonify({'message': UserMessages().UserDeleted(patient)})
