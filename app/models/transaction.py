from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    courier_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)

    outbox_entries = relationship("Outbox", back_populates="transaction")
