from typing import Any, Optional
from pydantic import BaseModel


class TransactionRequest(BaseModel):
    courier_id: int
    amount: float
