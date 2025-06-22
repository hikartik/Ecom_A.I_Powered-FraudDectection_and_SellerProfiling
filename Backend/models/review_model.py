# models/review_model.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    customer_id: str
    comment: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)

class Review(BaseModel):
    id: str = Field(alias="_id")
    product_id: str
    seller_id: str
    customer_id: str
    comment: Optional[str] = None
    rating: int
    rating_score: float = 0.0
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "60f5a4b4c2a97a6e9e8b4567",
                "product_id": "60f5a4b4c2a97a6e9e8b1234",
                "seller_id": "60f5a4b4c2a97a6e9e8b7890",
                "customer_id": "60f5a4b4c2a97a6e9e8b1122",
                "comment": "Great product!",
                "rating": 4,
                "rating_score": 0.0,
                "created_at": "2025-06-22T12:00:00Z"
            }
        }