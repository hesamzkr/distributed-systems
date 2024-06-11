from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

sql_engine = create_engine(
    config.SQL_URI, echo=False, isolation_level="REPEATABLE READ"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sql_engine)


def get_sql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
