from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime

class Product(BaseModel):
    seller_id: str
    product_name:str
    description: Optional[str] = None
    images: List[str] = []  # ✅ Cloudinary URLs
    realtime_score1: int = 0
    realtime_score2: int = 0
    realtime_score3: int = 0
    realtime_score4: int = 0
    batch_score: int = 0
    status: Literal["valid", "blocked_batch", "blocked_ai"] = "valid"
    created_at: datetime = Field(default_factory=datetime.now)
