from fastapi import APIRouter, Depends

from controllers.courier_controller import (
    collect_cash_controller,
    get_outboxes_controller,
    get_transactions_controller,
)
from db import get_all_dbs, get_db, get_db_for_transaction
from schemas.courier_schemas import TransactionRequest
from sqlalchemy.orm import Session

router = APIRouter(prefix="/courier")


@router.post("/collect_cash")
async def collect_cash(
    transaction_request: TransactionRequest,
    db: Session = Depends(get_db_for_transaction),
):
    return await collect_cash_controller(transaction_request, db)


@router.get("/transactions")
async def get_transactions(dbs=Depends(get_all_dbs)):
    async with dbs as sessions:
        return await get_transactions_controller(sessions)


@router.get("/outboxes")
async def get_outboxes(dbs=Depends(get_all_dbs)):
    async with dbs as sessions:
        return await get_outboxes_controller(sessions)
