from models.transaction import Transaction
from schemas.courier_schemas import TransactionRequest
from sqlalchemy.orm import Session
from utils import make_request_with_retries, breaker


async def collect_cash_controller(transaction_request: TransactionRequest, db: Session):
    transaction = Transaction(
        courier_id=transaction_request.courier_id,
        amount=transaction_request.amount,
        status="pending",
    )
    db.add(transaction)
    db.commit()

    try:
        json_payload = {
            "amount": transaction_request.amount,
            "currency": "EUR",
            "description": f"Courier collecting cash {transaction_request.courier_id}",
            "userId": str(transaction_request.courier_id),
        }

        @breaker
        async def send_transaction():
            return await make_request_with_retries(
                "http://harbour-cloudcomputing:8080/v1/wallet/transaction", json_payload
            )

        response = await send_transaction()

        if response.status_code == 200:
            transaction.status = "processed"
        else:
            transaction.status = "failed"
    except Exception as e:
        transaction.status = "error"
        print(e)
        db.rollback()

    db.commit()
    return {"transaction_id": transaction.id, "status": transaction.status}
