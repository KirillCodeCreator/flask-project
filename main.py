import requests
from flask import Flask, render_template, redirect, flash, request, make_response, jsonify, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_restful import Api
from waitress import serve

from api import doctor_api, patient_api, appointment_api, appointmentpatient_api
from api.specialization.specialization_resource import add_api_specializations_routes
from config import GEO_API_KEY, GEO_API_URL, STATIC_MAPS_URL
from data import db_session
from data.appointment import Appointment
from data.appointmentpatient import AppointmentPatient
from data.data_seed import init_data_to_db
from data.role import Roles
from data.timeinterval import TimeInterval
from data.users import User
from forms.appointment_result import AppointmentResultForm
from forms.create_appointment import CreateAppointmentForm
from forms.login import LoginForm
from forms.register_doctor import RegisterDoctorForm
from forms.register_patient import RegisterPatientForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask_project_secret_key'
app.config['DATETIME_FORMAT'] = '%Y-%m-%d'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager(app)
login_manager.login_message = "Авторизация успешно выполнена"
login_manager.init_app(app)
api = Api(app)

patient_menu = [{"url": "show_patient_appointments", "title": "Журнал запиcей"},
                {"url": "show_available_appointments_wall", "title": "Записаться"},
                {"url": "patient_help", "title": "Помощь пациенту"}]
doctor_menu = [{"url": "show_doctor_appointments", "title": "Журнал приемов"},
               {"url": "doctor_appointment_create", "title": "Создать прием"},
               {"url": "doctor_help", "title": "Помощь доктору"}]
admin_menu = [{"url": "doctor_wall", "title": "Список докторов"},
              {"url": "patient_wall", "title": "Список пациентов"},
              {"url": "appointments_wall", "title": "Журнал приемов и записей"}]


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/register-doctor", methods=['GET', 'POST'])
def register_doctor():
    if current_user.is_authenticated:
        if not current_user.is_doctor():
            return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
        return redirect(url_for('show_doctor_appointments'))
    form = RegisterDoctorForm()
    resp = requests.get(f'{request.host_url}/api/specializations')
    if not resp:
        message = resp.json()["message"]
        flash(message, "danger")
        return make_response(jsonify(f'message: {message}'), 404)
    specializations = resp.json()['specializations']
    specializations_list = [(i["id"], i["title"]) for i in specializations]
    form.specialization.choices = specializations_list

    if form.validate_on_submit():
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            middlename=form.middlename.data,
            birthday=form.birthday.data,
            location=form.location.data,
            specialization_id=int(form.specialization.data),
            phone=form.phone.data,
            email=form.login.data,
            hashed_password=form.password.data,
            role=Roles.DOCTOR,
        )
        user.set_password(form.password.data)

        resp = requests.post(f'{request.host_url}/api/doctors', json=user.to_dict())
        if resp.status_code == 200:
            message = resp.json()["message"]
            flash(message, "info")
            return redirect(url_for('login'))
        elif resp.status_code == 500:
            message = "Регистрация не завершена, обратитесь к системному администратору"
            flash(message, "error")
            return redirect(url_for('register_patient'))
        else:
            message = resp.json()["message"]
            flash(message, "danger")
            return redirect(url_for('register_doctor'))

    return render_template("register_doctor.html", title="Регистрация доктора", form=form)


@app.route('/register-patient', methods=['GET', 'POST'])
def register_patient():
    if current_user.is_authenticated:
        if not current_user.is_patient():
            return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
        return redirect(url_for('show_patient_appointments'))
    form = RegisterPatientForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                middlename=form.middlename.data,
                birthday=form.birthday.data,
                location=form.location.data,
                polis=form.polis.data,
                phone=form.phone.data,
                email=form.login.data,
                hashed_password=form.password.data,
                role=Roles.PATIENT,
            )
            user.set_password(form.password.data)

            resp = requests.post(f'{request.host_url}/api/patients', json=user.to_dict())
            if resp.status_code == 200:
                message = resp.json()["message"]
                flash(message, "info")
                return redirect(url_for('login'))
            elif resp.status_code == 500:
                message = "Регистрация не завершена, обратитесь к системному администратору"
                flash(message, "error")
                return redirect(url_for('register_patient'))
            else:
                message = resp.json()["message"]
                flash(message, "danger")
                return redirect(url_for('register_patient'))

    return render_template('register_patient.html', title='Регистрация пациента', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data) and user.role in [Roles.ADMIN, Roles.DOCTOR, Roles.PATIENT]:
            login_user(user, remember=form.remember_me.data)
            if user.role == Roles.DOCTOR:
                return redirect(url_for('show_doctor_appointments'))
            elif user.role == Roles.PATIENT:
                return redirect(url_for('show_patient_appointments'))
            elif user.role == Roles.ADMIN:
                return redirect(url_for('doctor_wall'))
        flash("Неправильный логин или пароль", "danger")
        return render_template("login.html", form=form, title="Авторизация пользователя")
    return render_template("login.html", title="Авторизация пользователя", form=form)


@app.errorhandler(404)
def page_not_found(error):
    flash("Страница не найдена", "danger")
    if current_user.is_authenticated:
        if current_user.is_patient():
            return redirect(url_for('show_patient_appointments'))
        elif current_user.is_doctor():
            return redirect(url_for('show_doctor_appointments'))
        elif current_user.is_admin():
            return redirect(url_for('doctor_wall'))
    return redirect(url_for('login'))


@app.errorhandler(401)
def authErr(error):
    flash("Доступ к странице только для авторизованных пользователей", "danger")
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/patient/appointmentpatients')
@login_required
def show_patient_appointments():
    if current_user.role != Roles.PATIENT:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)

    resp = requests.get(f'{request.host_url}api/appointmentpatients/patient/{current_user.id}')
    appointmentpatients = resp.json()["appointmentpatients"]
    return render_template('patient_appointments.html', title="Ваши записи к врачам",
                           appointmentpatients=appointmentpatients, menu=patient_menu)


@app.route('/patient/available-appointments-wall', methods=['GET', 'POST'])
@login_required
def show_available_appointments_wall():
    if current_user.role != Roles.PATIENT:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    db_sess = db_session.create_session()
    appointments = db_sess.query(Appointment).order_by(Appointment.date).all()
    appointmentPatientIds = [i.id for i in db_sess.query(Appointment).join(AppointmentPatient,
                                                                           Appointment.id == AppointmentPatient.appointment_id).all()]
    list = []
    for appointment in appointments:
        if not appointment.id in appointmentPatientIds:
            list.append(appointment)

    sorted_list = sorted(list, key=lambda a: (a.date, a.doctor.lastname, a.timeinterval.starttime))
    return render_template('patient_appointment_create.html', appointments=sorted_list, menu=patient_menu,
                           title="Доступные специалисты и приемы для записи")


@app.route('/patient/appointment/create/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def patient_appointment_create(appointment_id):
    if current_user.role != Roles.PATIENT:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    payload = {}
    payload["appointment_id"] = appointment_id
    payload["patient_id"] = current_user.id

    resp = requests.post(f'{request.host_url}api/appointmentpatients',
                         json={"appointment_id": f"{appointment_id}", "patient_id": f"{current_user.id}"})
    if resp.status_code == 200:
        message = resp.json()["message"]
        flash(message, "info")
    elif resp.status_code == 500:
        message = "Запись не завершена, обратитесь к системному администратору"
        flash(message, "error")
    else:
        message = resp.json()["message"]
        flash(message, "danger")
    return redirect(url_for('show_patient_appointments'))


@app.route('/patient/appointments/cancel/<int:patientappointment_id>')
@login_required
def patient_appointment_cancel(patientappointment_id):
    if current_user.role != Roles.PATIENT:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    resp = requests.delete(f'{request.host_url}api/appointmentpatients/{patientappointment_id}')
    if resp.status_code == 200:
        flash("Запись к врачу была успешно отменена", "info")
    elif resp.status_code == 500:
        flash("Ошибка при удалении записи к врачу", "error")

    resp = requests.get(f'{request.host_url}api/appointmentpatients/patient/{current_user.id}')
    appointmentpatients = resp.json()["appointmentpatients"]
    return render_template('patient_appointments.html', title="Ваши записи к врачам",
                           appointmentpatients=appointmentpatients, menu=patient_menu)


@app.route('/patient/appointments/show_map/<int:patientappointment_id>')
@login_required
def patient_appointment_show_map(patientappointment_id):
    if current_user.role != Roles.PATIENT:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    db_sess = db_session.create_session()
    appointmentpatient = db_sess.query(AppointmentPatient).filter(
        AppointmentPatient.id == patientappointment_id).first()
    if not appointmentpatient:
        flash("Не удалось отобразить адрес приема на карте", "warning")
        return redirect(url_for('show_patient_appointments'))

    location = appointmentpatient.appointment.doctor.location
    if len(location) > 0:
        geocoder_params = {
            "apikey": GEO_API_KEY,
            "geocode": location,
            "format": "json"
        }
        geocode_resp = requests.get(GEO_API_URL, params=geocoder_params)
        if not geocode_resp:
            flash(f"Не удалось отобразить адрес приема на карте: {location}", "warning")
            return redirect(url_for('show_patient_appointments'))
        geocode_json = geocode_resp.json()
        try:
            point = geocode_json["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]["Point"]["pos"]
        except (KeyError, IndexError):
            flash(f"Не удалось отобразить адрес приема на карте: {location}", "warning")
            return redirect(url_for('show_patient_appointments'))
        point = ",".join(point.split())
        map_static_params = {
            "ll": point,
            "l": "map",
            "z": 17,
            'lang': 'ru_RU',
            'pt': f'{point}'
        }
        map_url = requests.Request(url=STATIC_MAPS_URL,
                                   params=map_static_params).prepare().url
        return render_template("show_map.html", location=location, map_url=map_url, title="Адрес для посещения приема",
                               menu=patient_menu)
    else:
        flash("Адрес приема не задан, отображение на карте невозможно", "warning")
        return redirect(url_for('show_patient_appointments'))


@app.route('/doctor/appointments')
@login_required
def show_doctor_appointments():
    if current_user.role != Roles.DOCTOR:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)

    resp = requests.get(f'{request.host_url}api/doctors/appointmentpatients/{current_user.id}')
    if resp.status_code == 500:
        flash("Ошибка получения приемов к врачу", "danger")
    else:
        appointments = resp.json()["appointments"]
        return render_template('doctor_appointments.html', appointments=appointments, menu=doctor_menu,
                               title="Ваши приемы пациентов")


@app.route('/doctor/appointment/create', methods=['GET', 'POST'])
@login_required
def doctor_appointment_create():
    if current_user.role != Roles.DOCTOR:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)

    form = CreateAppointmentForm()
    db_sess = db_session.create_session()
    timeintervals = db_sess.query(TimeInterval).all()
    times = [(t.id, f'{t.starttime.strftime("%H:%M")} - {t.endtime.strftime("%H:%M")}') for t in timeintervals]

    form.time.choices = times

    if form.validate_on_submit():
        appointment = Appointment(
            date=form.date.data,
            doctor_id=current_user.id,
            timeinterval_id=int(form.time.data),
        )

        resp = requests.post(f'{request.host_url}api/appointments', json=appointment.to_dict())
        if resp.status_code == 200:
            message = resp.json()["message"]
            flash(message, "info")
        elif resp.status_code == 500:
            message = "Создание не завершено, обратитесь к системному администратору"
            flash(message, "danger")
        else:
            message = resp.json()["message"]
            flash(message, "danger")
        return redirect(url_for('show_doctor_appointments'))

    return render_template("doctor_appointment_create.html", title="Создание приема у доктора", form=form,
                           menu=doctor_menu)


@app.route('/doctor/appointment/finish/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def doctor_appointment_finish(appointment_id):
    if current_user.role != Roles.DOCTOR:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)

    form = AppointmentResultForm()
    db_sess = db_session.create_session()
    appointmentpatient = db_sess.query(AppointmentPatient).filter(
        AppointmentPatient.appointment_id == appointment_id).first()
    if not appointmentpatient:
        flash("Операция невозможна, на прием не записан пациент", category="warning")
        return redirect(url_for("show_doctor_appointments"))

    if appointmentpatient.result:
        form.appointmentresult.data = appointmentpatient.result

    if form.validate_on_submit():

        resp = requests.put(f'{request.host_url}api/appointmentpatients/{appointmentpatient.id}',
                            json={"result": form.appointmentresult.data})

        if resp.status_code == 200:
            message = resp.json()["message"]
            flash(message, "info")
        elif resp.status_code == 500:
            message = "Оформление результат не завершено, обратитесь к системному администратору"
            flash(message, "danger")
        else:
            message = resp.json()["message"]
            flash(message, "danger")
        return redirect(url_for("show_doctor_appointments"))
    return render_template("appointment_result.html", description=appointmentpatient.patient.full_name(),
                           title="Результат приема пациента", form=form, menu=doctor_menu)


@app.route('/profile')
@login_required
def show_profile():
    if current_user.role == Roles.DOCTOR:
        resp = requests.get(f'{request.host_url}api/doctors/{current_user.id}')
        if not resp:
            message = resp.json()["message"]
            flash(message, "danger")
            return make_response(jsonify(f'message: {message}'), 404)
        doctor = resp.json()["doctors"][0]
        return render_template('doctor_profile.html', user=doctor, menu=doctor_menu, title="Профиль доктора")
    elif current_user.role == Roles.PATIENT:
        resp = requests.get(f'{request.host_url}api/patients/{current_user.id}')
        if not resp:
            message = resp.json()["message"]
            flash(message, "danger")
            return make_response(jsonify(f'message: {message}'), 404)
        patient = resp.json()["patients"][0]
        return render_template('patient_profile.html', user=patient, menu=patient_menu, title="Профиль пациента")
    elif current_user.role == Roles.ADMIN:
        db_sess = db_session.create_session()
        admin = db_sess.query(User).filter(User.role == Roles.ADMIN).first()
        if not admin:
            flash("Просмотр страницы не доступен", "danger")
            return redirect('/')
        return render_template('admin_profile.html', user=admin, menu=admin_menu, title="Профиль администратора")

    flash("Просмотр страницы не доступен", "danger")
    return make_response(jsonify(f'Просмотр страницы не доступен'), 403)


@app.route('/doctors/wall')
@login_required
def doctor_wall():
    if current_user.role != Roles.ADMIN:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    resp = requests.get(f'{request.host_url}api/doctors')
    if not resp:
        message = resp.json()["message"]
        flash(message, "danger")
        return make_response(jsonify(f'message: {message}'), 404)
    doctors = resp.json()['doctors']
    return render_template('doctors_wall.html', menu=admin_menu, doctors=doctors, title="Список докторов")


@app.route('/patient-wall')
@login_required
def patient_wall():
    if current_user.role != Roles.ADMIN:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    resp = requests.get(f'{request.host_url}/api/patients')
    if not resp:
        message = resp.json()["message"]
        flash(message, "danger")
        return make_response(jsonify(f'message: {message}'), 404)
    patients = resp.json()['patients']
    return render_template('patients_wall.html', menu=admin_menu, patients=patients, title="Список пациентов")


@app.route('/appointments-wall')
@login_required
def appointments_wall():
    if current_user.role != Roles.ADMIN:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    db_sess = db_session.create_session()
    appointments_data = db_sess.query(Appointment).all()
    appointments = []
    for ap in appointments_data:
        appointmentPatients = db_sess.query(AppointmentPatient).filter(AppointmentPatient.appointment_id == ap.id).all()
        if appointmentPatients:
            for p in appointmentPatients:
                appointments.append({"date": p.appointment.date.strftime("%Y-%m-%d"),
                                     "time": p.appointment.timeinterval.starttime.strftime("%H:%M"),
                                     "spec": p.appointment.doctor.specialization.title,
                                     "doctor": p.appointment.doctor.full_name(),
                                     "patient": p.patient.full_name(),
                                     "result": p.result})
        else:
            appointments.append({"date": ap.date.strftime("%Y-%m-%d"),
                                 "time": ap.timeinterval.starttime.strftime("%H:%M"),
                                 "spec": ap.doctor.specialization.title,
                                 "doctor": ap.doctor.full_name(),
                                 "patient": "не назначен",
                                 "result": None})

    return render_template('appointments_wall.html', menu=admin_menu, appointments=appointments,
                           title="Список приемов и записей")


@app.route("/")
def main_page():
    if current_user.is_authenticated:
        if current_user.is_patient():
            return redirect(url_for('show_patient_appointments'))
        elif current_user.is_doctor():
            return redirect(url_for('show_doctor_appointments'))
        elif current_user.is_admin():
            return redirect(url_for('doctor_wall'))
    return render_template("index.html")


def main():
    db_session.global_init("data.db")
    init_data_to_db()
    app.register_blueprint(doctor_api.doctor_api)
    app.register_blueprint(patient_api.patient_api)
    app.register_blueprint(appointment_api.appointment_api)
    app.register_blueprint(appointmentpatient_api.appointmentpatient_api)
    add_api_specializations_routes(api)
    serve(app, host="0.0.0.0", port=5000)
    # app.run("", port=5000)


@app.route("/doctor-help")
def doctor_help():
    if current_user.role != Roles.DOCTOR:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    return render_template("doctor_help.html", title="Инструкция для доктора", menu=doctor_menu)


@app.route("/patient-help")
def patient_help():
    if current_user.role != Roles.PATIENT:
        return make_response(jsonify({"message": 'Sorry, you have no access to page'}), 403)
    return render_template("patient_help.html", title="Инструкция для пациента", menu=patient_menu)


if __name__ == '__main__':
    main()
