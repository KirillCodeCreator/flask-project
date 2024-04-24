# Проект "Онлайн поликлиника" 
Учебный проект WebServer + API в рамках обучения в яндекс лицее 

# Идея проекта
Разработать сервис для организации приемов и записей на приемы между докторами и пациентами. 


# Авторизация и аутентификация пользователей
* Реализована ролевая модель разграничения доступа. В проекте используется три роли: администратор, доктор и пациент.
* При старте web сервера происходит инициализация 3х пользователей по умолчанию:
  - Администратор, логин admin@mail.ru
  - Доктор, логин doctor@mail.ru
  - Пациент, логин patient@mail.ru
* Для новых пользователей доступна регистрация в качестве доктора или пациента. После регистрации у каждого пользователя будет свой личный кабинет. Пароли храняться в бд в виде хеш кода
* Доступна возможность просматривать свой профиль.
* Для пользователей каждой из ролей набор доступных действий и пунктов меню в личном кабинете различен.
* Администратор может просматривать списки докторов, списки пацинетов, журнал приемов и записанных на них пациентов.

# Система помощи пользователям
* В личных кабинетах пользователей есть специальный раздел "Помощь", перейдя в который пользователь сможет ознакомиться с основным функционалом его личного кабинета.
* Раздел помощи для доктора и пациента различаются по содержанию.

# Стек технологий
* Языки Python и js
* Фреймворк flask
* Библиотеки flask-wtf, blueprint, Flask-SQLAlchemy, flask-login, flask-restful, flask-wtf, bootstrap-flask, requests, Jinja2, SQLAlchemy-serializer, Werkzeug и др.
* WSGI-сервер waitress

# Работа с внешними сервисами и другие функции
* Реализовано взаимодействие с сервисами API Yandex Maps 
* Выполняются http rest запросы и обработка данных от сервисов yandex:
  - http://geocode-maps.yandex.ru/1.x/ для получения координат по адресу
  - https://static-maps.yandex.ru/1.x/ для получения изображения участка карты по полученным координатам на местности
* Загрузка изображений из ресурсов проекта для профилей пользователей
* Чтение json файла инициализации специализаций докторов и внесение этих данных в бд.

# База данных
В проекте использована база данных sqlite. Работа с бд происходит с применением ORM SQLAlchemy (Flask-SQLAlchemy) через разработанные нами классы в проекте.

# Хостинг в сети интернет
* Web сервер размещен на хостинге в сети интернет по адресу http://195.49.187.78:9000/ и доступен извне (порт указывать обязательно).
* В связи с тем, что хостинг бесплатный, то без предупреждения сервис может быть выключен.
* В случае недоступности сервиса следует связаться с авторами проекта и доступ будет восстановлен в короткое время

# Локальная сборка и запуск
Доступна локальная сборка и запуск сервера. Для этого склонируйте данный репозиторий (ветка main)
* Зависимости: `pip install -r requirements.txt`
* Запуск `python main.py`

# Авторы
* Лоторев Кирилл
* Шумакова Яна
