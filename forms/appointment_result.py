from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class AppointmentResultForm(FlaskForm):
    appointmentresult = StringField("Результат приема", validators=[InputRequired("обязательное поле")])
    submit = SubmitField('Сохранить')
