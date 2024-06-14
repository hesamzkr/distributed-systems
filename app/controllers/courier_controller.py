from fastapi import HTTPException
from models.transaction import Transaction
from schemas.courier_schemas import TransactionRequest
from sqlalchemy.orm import Session
import requests


def collect_cash_controller(transaction_request: TransactionRequest, db: Session):
    try:
        transaction = Transaction(
            courier_id=transaction_request.courier_id,
            amount=transaction_request.amount,
            status="pending",
        )
        db.add(transaction)

        try:
            response = requests.post(
                "http://harbour-cloudcomputing:8080/v1/wallet/transaction",
                json={
                    "amount": transaction_request.amount,
                    "currency": "EUR",
                    "description": f"Courier collecting cash {transaction_request.courier_id}",
                    "userId": str(transaction_request.courier_id),
                },
            )
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
