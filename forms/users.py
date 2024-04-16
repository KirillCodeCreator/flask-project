from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired, EqualTo, NumberRange
from wtforms.validators import ValidationError

from data import db_session
from data.users import User


class RegisterDoctorForm(FlaskForm):
    login = EmailField("Login / email", validators=[DataRequired()])

    def validate_login(form, field):
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == field.data).first():
            raise ValidationError("Такой пользователь уже существует")

    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat Password",
                                    validators=[EqualTo("password", "Пароли должны совпадать")])
    firstname = StringField("Firstname")
    lastname = StringField("Lastname")
    datebirth = DateField('Date', format='/%d/%m/%Y')
    position = StringField("Position")
    speciality = StringField("Speciality")
    address = StringField("Address")
    city_from = StringField("City From")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
