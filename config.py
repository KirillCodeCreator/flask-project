import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP_NAME = "app"
APP_DIR = os.path.join(BASE_DIR, APP_NAME)
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'data.db')}"
SECRET_KEY = "yandexlyceum_secret_key"
GEO_API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
GEO_API_URL = "http://geocode-maps.yandex.ru/1.x/"