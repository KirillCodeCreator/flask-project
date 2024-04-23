import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateField
from wtforms.validators import InputRequired, ValidationError


class CreateAppointmentForm(FlaskForm):
    def validate_date(form, field):
        if field.data <= datetime.datetime.now().date():
            raise ValidationError("Дата не может быть ранее, чем за один день до начала приема")

    date = DateField('Дата приема', format='%Y-%m-%d', validators=[InputRequired("обязательное поле")])
    time = SelectField("Время", validators=[InputRequired("обязательное поле")])
    submit = SubmitField("Опубликовать прием")
