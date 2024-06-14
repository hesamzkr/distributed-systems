from sqlalchemy import create_engine
from config import config
from models.base import Base

engine = create_engine(config.SQL_URI.replace("@mysql", "@localhost"))
Base.metadata.create_all(bind=engine)

print("Successfully created tables")
