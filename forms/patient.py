from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, NumberRange
from wtforms.validators import ValidationError

from data import db_session
from data.users import User


class PatientForm(FlaskForm):
    login = EmailField("Логин пациента", validators=[DataRequired()])

    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль",
                                    validators=[EqualTo("password", "Пароли должны совпадать")])
    surname = StringField("Фамилия")
    name = StringField("Имя")
    age = IntegerField("Возраст", validators=[NumberRange(1, 99)])
    submit = SubmitField("Submit")
    '''
        def validate_login(form, field):
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == field.data).first():
                raise ValidationError("Такой пользователь уже существует")
    '''


class LoginForm(FlaskForm):
    email = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
