import json
import datetime

from werkzeug.security import generate_password_hash

from data import db_session
from data.role import Roles
from data.specialization import Specialization
from data.timeinterval import TimeInterval
from data.users import User


def get_users_data():
    users_data = [
        {
            "firstname": "Иван",
            "lastname": "Иванов",
            "role": Roles().ADMIN,
            "phone": "+79102222222",
            "email": "admin@mail.ru",
            "hashed_password": generate_password_hash("admin"),
            "modified_date": datetime.now()
        }
    ]
    return users_data


def create_admin_user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.role == Roles().ADMIN).all()
    if user:
        return
    users = get_users_data()
    for user_data in users:
        user = User(**user_data)
        db_sess.add(user)
    db_sess.commit()


def get_specializations_data():
    with open("data/specializations.json", "r", encoding="utf-8") as read_file:
        return json.load(read_file)


def create_specialization():
    db_sess = db_session.create_session()
    specializations_data = get_specializations_data()
    specializations = db_sess.query(Specialization).all()
    specializations = [specialization.title for specialization in specializations]
    for specialization_data in specializations_data['specializations']:
        if specialization_data['title'] in specializations:
            continue
        specialization = Specialization(**specialization_data)
        db_sess.add(specialization)

    db_sess.commit()

def create_timeintervals():
    db_sess = db_session.create_session()
    timeintervals = db_sess.query(TimeInterval).all()
    times = [timeinterval.starttime for timeinterval in timeintervals]
    starttime = datetime.time(8, 0, 0)
    halftimedelta = datetime.timedelta (minutes=30)
    hourtimedelta = datetime.timedelta(hours=1)
    for i in range(0, 10):
        if starttime in times:
            continue
        timeinterval = TimeInterval()
        timeinterval.starttime = starttime

        tmp_datetime = datetime.datetime.combine(datetime.date(1, 1, 1), starttime)
        timeinterval.endtime = (tmp_datetime + halftimedelta).time()

        starttime = (tmp_datetime + hourtimedelta).time()
        db_sess.add(timeinterval)

    db_sess.commit()

def init_data_to_db():
    create_admin_user()
    create_specialization()
    create_timeintervals()
