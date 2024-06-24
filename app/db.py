from contextlib import AsyncExitStack, asynccontextmanager, contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schemas.courier_schemas import TransactionRequest
from config import config

sql_engine = create_engine(config.SQL_URI, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sql_engine)

sql_engine_2 = create_engine(config.SQL_URI_2, echo=False)
SessionLocal_2 = sessionmaker(autocommit=False, autoflush=False, bind=sql_engine_2)


async def get_db_for_transaction(transaction_request: TransactionRequest):
    async with AsyncExitStack() as stack:
        db = stack.enter_context(get_db(transaction_request.courier_id))
        yield db


@asynccontextmanager
async def get_all_dbs():
    async with AsyncExitStack() as stack:
        db = stack.enter_context(get_db(1))
        db2 = stack.enter_context(get_db(2))
        yield [db, db2]


@contextmanager
def get_db(courier_id: int):
    if courier_id % 2 == 0:
        db = SessionLocal()
    else:
        db = SessionLocal_2()
    try:
        yield db
    finally:
        db.close()
