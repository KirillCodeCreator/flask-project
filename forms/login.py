from flask import url_for
from flask_wtf import FlaskForm
from wtforms import EmailField, BooleanField, PasswordField, SubmitField, URLField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')