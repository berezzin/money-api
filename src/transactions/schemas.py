from pydantic import BaseModel, Field


class TransactionSchema(BaseModel):
    transaction_comment: str | None = Field(max_length=50, default=None)
    transaction_amount: float = 0
    transaction_category: int
