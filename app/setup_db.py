from sqlalchemy import create_engine
from config import config
from models.base import Base
from models.transaction import Transaction

transaction = Transaction()

engine = create_engine(config.SQL_URI.replace("@mysql:3306", "@localhost:3306"))
Base.metadata.create_all(bind=engine)

engine2 = create_engine(config.SQL_URI_2.replace("@mysql2:3306", "@localhost:3307"))
Base.metadata.create_all(bind=engine2)


print("Successfully created tables")
