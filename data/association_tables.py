#import sqlalchemy as sa

from app import db
#from data.db_session import SqlAlchemyBase

#ассоциация для специализации и пользователя
specialization_users_table = db.Table("specialization_users", db.metadata,
                             db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                             db.Column("specialization_id", db.Integer, db.ForeignKey("specialization.id")))

#таблица для связи роли и пользователя
role_users_table = db.Table("role_users", db.metadata,
                             db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                             db.Column("role_id", db.Integer, db.ForeignKey("role.id")))