from fastapi import APIRouter, Depends

from controllers.courier_controller import collect_cash_controller
from db import get_db_for_transaction
from schemas.courier_schemas import TransactionRequest
from sqlalchemy.orm import Session

router = APIRouter(prefix="/courier")


@router.post("/collect_cash")
async def collect_cash(
    transaction_request: TransactionRequest,
    db: Session = Depends(get_db_for_transaction),
):
    return await collect_cash_controller(transaction_request, db)
