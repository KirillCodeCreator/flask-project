import json
from datetime import datetime

from werkzeug.security import generate_password_hash

from data import db_session
from data.role import Roles
from data.specialization import Specialization
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


def get_jobs_data():
    jobs_data = [
        {
            "team_leader_id": 1,
            "job": "Deployment of residential modules 1 and 2",
            "work_size": 15,
            "collaborators": "2, 3",
            "start_date": datetime.now(),
            "categories": [1],
            "is_finished": False,
        },
        {
            "team_leader_id": 2,
            "job": "Exploration of mineral sources",
            "work_size": 15,
            "collaborators": "4, 3",
            "start_date": datetime.now(),
            "categories": [2],
            "is_finished": False,
        },
        {
            "team_leader_id": 3,
            "job": "Development of management system",
            "work_size": 25,
            "collaborators": "5",
            "start_date": datetime.now(),
            "categories": [1, 3],
            "is_finished": False,
        },
        {
            "team_leader_id": 4,
            "job": "Fix ventilation system",
            "work_size": 20,
            "collaborators": "2, 5",
            "start_date": datetime.now(),
            "categories": [1],
            "is_finished": True,
        },
    ]
    return jobs_data


'''
def create_jobs():
    db_sess = db_session.create_session()
    jobs = get_jobs_data()
    for job_data in jobs:
        categories_id = job_data.pop("categories")
        categories = []
        for category_id in categories_id:
            category = db_sess.get(Category, category_id)
            categories.append(category)
        job = Jobs(**job_data)
        for category in categories:
            job.categories.append(category)
        db_sess.add(job)
    db_sess.commit()
'''

def init_data_to_db():
    create_admin_user()
    create_specialization()
