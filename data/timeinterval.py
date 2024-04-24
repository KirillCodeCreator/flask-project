from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
import sqlalchemy as sa


class TimeInterval(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "timeinterval"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    starttime = sa.Column(sa.Time, nullable=False) #время начала консультации
    endtime = sa.Column(sa.Time, nullable=False) #время окончания консультации

    def full_time(self):
        return f"{self.starttime.strftime('%H:%M')} - {self.endtime.strftime('%H:%M')}"

    def __repr__(self):
        return f"{self.starttime} - {self.endtime}"