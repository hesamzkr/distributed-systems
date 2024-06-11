from fastapi import APIRouter

from schemas.wallet_schemas import GenericResponse, TransactionRequest


router = APIRouter()


@router.post("/v1/wallet/transaction", response_model=GenericResponse)
async def create_transaction(transaction: TransactionRequest):
    # Placeholder for actual transaction creation logic
    response = GenericResponse(
        data={"transactionId": "12345", "status": "success"}, error=None
    )
    return response
