from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Email
from wtforms.validators import ValidationError

from data import db_session
from data.users import User


class RegisterDoctorForm(FlaskForm):
    login = StringField("Логин / email", validators=[InputRequired(), Email()])

    def validate_login(form, field):
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == field.data).first():
            raise ValidationError("Такой пользователь уже существует")

    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль",
                                    validators=[EqualTo("password", "Пароли должны совпадать")])
    firstname = StringField("Имя", validators=[InputRequired("обязательное поле")])
    lastname = StringField("Фамилия", validators=[InputRequired("обязательное поле")])
    middlename = StringField("Отчество", validators=[InputRequired("обязательное поле")])
    birthday = DateField('Дата рождения', format='%Y-%m-%d', validators=[InputRequired("обязательное поле")])
    phone = StringField("Телефон", validators=[InputRequired("обязательное поле")])
    location = StringField("Адрес работы", validators=[InputRequired("обязательное поле")])
    specialization = SelectField("Специальность", validators=[InputRequired("обязательное поле")])
    submit = SubmitField("Зарегистрироваться")
