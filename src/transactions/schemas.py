from pydantic import BaseModel, Field


class TransactionSchema(BaseModel):
    user_id: str = Field(min_length=32, max_length=36)
    transaction_comment: str | None = Field(max_length=50, default=None)
    transaction_amount: float = 0
    transaction_category: int
