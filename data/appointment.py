from data.db_session import SqlAlchemyBase
from datetime import datetime
from sqlalchemy import orm
import sqlalchemy as sa

# класс для таблицы консультаций
class Appointment(SqlAlchemyBase):
    __tablename__ = "appointment"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date = sa.Column(sa.Date, default=datetime.today(), nullable=False) #дата консультации
    time = sa.Column(sa.Time, nullable=False) #время консультации
    duration = sa.Column(sa.Integer, default=15, nullable=False)  # длительность
    doctor_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False) # id доктора
    doctor = orm.relationship("User")
    location = sa.Column(sa.String, nullable=False) #адрес консультации

    def __repr__(self):
        return f"<Jobs {self.id} {self.doctor} {self.date} {self.time} {self.location}>"