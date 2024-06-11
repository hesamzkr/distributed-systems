from typing import Any, Optional
from pydantic import BaseModel


class TransactionRequest(BaseModel):
    amount: float
    currency: str
    description: str
    userId: str


class GenericResponse(BaseModel):
    data: Optional[Any]
    error: Optional[str] = None


class TransactionResponse(BaseModel):
    transactionId: str
    status: str
