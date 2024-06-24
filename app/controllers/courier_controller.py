import asyncio
import json

from sqlalchemy import func
from db import SessionLocal, SessionLocal_2
from models.outbox import Outbox
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

        outbox_entry = Outbox(
            transaction_id=transaction.id,
            payload=json.dumps(json_payload),
            status="pending",
        )
        db.add(outbox_entry)
        db.commit()

        transaction.status = "outbox"
        db.commit()
    except Exception as e:
        transaction.status = "error"
        db.rollback()
        print(e)

    return {"transaction_id": transaction.id, "status": transaction.status}


async def process_outbox():
    while True:
        with SessionLocal() as session1, SessionLocal_2() as session2:
            for session in [session1, session2]:
                outbox_entries = session.query(Outbox).filter_by(status="pending").all()
                for entry in outbox_entries:
                    try:

                        @breaker
                        async def send_transaction():
                            return await make_request_with_retries(
                                "http://harbour-cloudcomputing:8080/v1/wallet/transaction",
                                json.loads(entry.payload),
                            )

                        response = await send_transaction()

                        if response.status_code == 200:
                            entry.status = "processed"
                            transaction = (
                                session.query(Transaction)
                                .filter_by(id=entry.transaction_id)
                                .first()
                            )
                            transaction.status = "processed"
                        else:
                            entry.status = "failed"
                    except Exception as e:
                        entry.status = "error"
                        print(e)

                    session.commit()

        await asyncio.sleep(5)


async def get_transactions_controller(sessions: list[Session]):
    transactions = []
    for db in sessions:
        transactions.extend(db.query(Transaction).all())
    return transactions


async def get_outboxes_controller(sessions: list[Session]):
    outboxes = []
    for db in sessions:
        outboxes.extend(db.query(Outbox).all())
    return outboxes
