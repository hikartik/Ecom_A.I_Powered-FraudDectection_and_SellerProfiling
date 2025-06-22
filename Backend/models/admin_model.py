from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class UserOutAdmin(BaseModel):
    id: str
    name: str
    email: str
    type: Literal["seller", "admin", "customer"]
    score: Optional[float] = 0.0
    created_at: Optional[datetime]
    is_banned: Optional[bool] = False

class ProductOutAdmin(BaseModel):
    id: str = Field(alias="_id")
    seller_id: str
    product_name: str
    description: Optional[str] = None
    images: List[str] = []
    vision_score: float = 0.0
    text_score: float = 0.0
    multimodal_score: float = 0.0
    ensemble_score: float = 0.0
    risk_label: str
    batch_score: float = 0.0
    status: Literal["valid", "blocked_batch", "blocked_ai"]
    created_at: datetime

    class Config:
        allow_population_by_field_name = True

class ProductUpdateAdmin(BaseModel):
    ensemble_score: Optional[float]
    status: Optional[Literal["valid", "blocked_batch", "blocked_ai"]]

class UserDetailWithProducts(BaseModel):
    user: UserOutAdmin
    products: List[ProductOutAdmin]
