import requests
from flask import Flask, render_template, redirect, flash, request, abort, url_for, make_response, jsonify
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_restful import Api

from api import jobs_api, users_api
from api.jobs_resource import init_api_v2_routes_jobs
from api.users_resource import init_api_v2_routes
from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.departments import AddDepartmentForm
from forms.jobs import AddJobForm
from forms.users import RegisterForm, LoginForm
from forms.patient import PatientForm
from data.patients import Patients

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/add-job", methods=["GET", "POST"])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader_id=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/jobs-wall")
    return render_template("add_job.html", form=form, title="Adding a job")


@app.route("/edit-job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id). \
            filter((Jobs.team_leader == current_user) | (current_user.id == 1)).first()
        if job:
            form.team_leader.data = job.team_leader_id
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id). \
            filter((Jobs.team_leader == current_user) | (current_user.id == 1)).first()
        if job:
            job.team_leader_id = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template("add_job.html", title="Редактирование работы", form=form)


@app.route("/delete-job/<int:job_id>", methods=["GET", "POST"])
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id). \
        filter((Jobs.team_leader == current_user) | (current_user.id == 1)).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/jobs-wall")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            city_from=form.city_from.data,
            email=form.login.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route('/reg_pat', methods=['GET', 'POST'])
def reg_pat():
    form = PatientForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        patient = Patients(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            email=form.login.data
        )
        patient.set_password(form.password.data)
        db_sess.add(patient)
        db_sess.commit()
        return redirect('/admin')
    return render_template('reg_pat.html', title='Пациент', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/jobs-wall")
        flash("Неправильный логин или пароль", "danger")
        return render_template("login.html", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/admin')
def admin_page():
    return render_template('admin.html')


@app.route("/add-department", methods=["GET", "POST"])
@login_required
def add_department():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Department).filter(Department.email == form.email.data).first():
            flash("Такой департамент уже существует", "danger")
            return redirect("/add-department")
        department = Department(
            title=form.title.data,
            chief_id=form.chief_id.data,
            members=form.members.data,
            email=form.email.data,
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect("/departments")
    return render_template("add_department.html", title="Добавить работу", form=form)


@app.route("/edit-department/<int:department_id>", methods=["GET", "POST"])
@login_required
def edit_department(department_id):
    form = AddDepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id) \
            .filter((Department.chief == current_user) | (current_user.id == 1)).first()
        if department:
            form.title.data = department.title
            form.chief_id.data = department.chief_id
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id) \
            .filter((Department.chief == current_user) | (current_user.id == 1)).first()
        if department:
            department.title = form.title.data
            department.chief_id = form.chief_id.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect("/departments")
        else:
            abort(404)
    return render_template("add_department.html", title="Изменить работу", form=form)


@app.route("/delete-department/<int:department_id>")
@login_required
def delete_department(department_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id) \
        .filter((Department.chief == current_user) | (current_user.id == 1)).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/departments")


@app.route("/departments")
def departments_list():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template("departments_list.html", departments=departments)


@app.route("/")
def main_page():
    '''
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("work_log.html", jobs=jobs)'''
    return render_template("main.html")


@app.route("/choice")
def choice_page():
    return render_template('choice.html')


@app.route("/jobs-wall")
def work_log():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("work_log.html", jobs=jobs)


@app.route("/users_show/<int:user_id>")
def users_show(user_id):
    resp = requests.get(f'{request.host_url}{url_for("users_api.get_user", user_id=user_id)}')
    if not resp:
        err = resp.json()["error"]
        return make_response(jsonify(f'Error: {err}'), 404)
    user = resp.json()["users"][0]
    user_city = user["city_from"]
    if len(user_city) > 0:
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": user_city,
            "format": "json"
        }
        geocode_resp = requests.get("http://geocode-maps.yandex.ru/1.x/", params=geocoder_params)
        if not geocode_resp:
            user['city_from'] = f"Geocoder for '{user_city}': {geocode_resp.status_code}. {geocode_resp.reason}"
            return render_template("user.html", user_data=user)
        geocode_json = geocode_resp.json()
        try:
            point = geocode_json["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]["Point"]["pos"]
        except (KeyError, IndexError):
            return render_template("user.html", user_data=user)
        point = ",".join(point.split())
        map_static_params = {
            "ll": point,
            "l": "sat",
            "z": 13,
        }
        map_url = requests.Request(url="https://static-maps.yandex.ru/1.x/",
                                   params=map_static_params).prepare().url
        return render_template("user_city.html", user_data=user, map_url=map_url)
    else:
        user['city_from'] = 'empty'
        return render_template("user.html", user_data=user)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    init_api_v2_routes(api)
    init_api_v2_routes_jobs(api)
    app.run("", port=8080)


@app.route("/help")
def help_page():
    return render_template("help.html")


if __name__ == '__main__':
    main()
