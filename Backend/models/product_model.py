from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime

class Product(BaseModel):
    seller_id: str
    product_name:str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Product price in currency units")
    images: List[str] = []  # ✅ Cloudinary URLs
    vision_score: float = 0.0
    text_score: float = 0.0
    multimodal_score: float = 0.0
    ensemble_score: float = 0.0
    risk_label:str
    batch_score: float = 0.0
    status: Literal["valid", "blocked_batch", "blocked_ai"] = "valid"
    created_at: datetime = Field(default_factory=datetime.now)
