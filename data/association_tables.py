import sqlalchemy as sa

from data.db_session import SqlAlchemyBase

#ассоциация для специализации и пользователя
specialization_users_table = sa.Table("specialization_users", SqlAlchemyBase.metadata,
                             sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id")),
                             sa.Column("specialization_id", sa.Integer, sa.ForeignKey("specialization.id")))

#таблица для связи роли и пользователя
role_users_table = sa.Table("role_users", SqlAlchemyBase.metadata,
                             sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id")),
                             sa.Column("role_id", sa.Integer, sa.ForeignKey("role.id")))