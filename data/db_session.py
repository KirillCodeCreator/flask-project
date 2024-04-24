import os

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None

DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "100"))
WEB_CONCURRENCY = int(os.getenv("WEB_CONCURRENCY", "2"))
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

def global_init(db_file):
    global __factory
    if __factory is not None:
        return
    if not db_file or not db_file.strip():
        raise ValueError("Необходимо указать файл БД")
    conn_str = f"sqlite:///{db_file.strip()}?check_same_tread=False"
    engine = sa.create_engine(conn_str, echo=False, pool_size=POOL_SIZE, max_overflow=0)
    __factory = orm.sessionmaker(bind=engine)
    print(f"Подключение к БД: {conn_str} ...")
    SqlAlchemyBase.metadata.create_all(engine)
    print(f"Подключено к БД: sqlite:///{db_file.strip()}")

def create_session() -> Session:
    global __factory
    return __factory()
