from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional
from uuid import uuid4
from datetime import datetime
import asyncio
from database import get_db

class Product(BaseModel):
    seller_id: str
    description: Optional[str] = None
    image: Optional[str] = None        # URL or base64 string
    realtime_score1: int
    realtime_score2: int
    realtime_score3: int
    realtime_score4: int                # 1–4
    batch_score: int                   # 1–4
    status: Literal["valid", "blocked_batch", "blocked_ai"] = "valid"
    created_at: datetime = Field(default_factory=datetime.now)

 

async def test_product_model_and_db():
    db = get_db()
    products = db["products"]

    # Ensure our indexes exist
    await products.create_index("seller_id")
    await products.create_index("status")

    # 1) Validate model instantiation
    try:
        dummy = Product(
            seller_id="seller_abc_123",
            description="A test product for QA",
            image="https://example.com/img.png",
            realtime_score1=1,
            realtime_score2=2,
            realtime_score3=3,
            realtime_score4=4,
            batch_score=2,
            status="valid",
        )
    except ValidationError as exc:
        print("❌ Validation error:", exc)
        return

    print("✅ Generated Product model:")
    print(dummy.model_dump_json(indent=2))

    # 2) Insert into MongoDB
    data = dummy.model_dump()
    insert_result = await products.insert_one(data)
    print(f"🆔 Inserted document _id = {insert_result.inserted_id!r}")

    # 3) Fetch & verify
    fetched = await products.find_one({"_id": insert_result.inserted_id})
    print("🔄 Fetched document from Mongo:")
    print(fetched)

    # 4) Cleanup
    await products.delete_one({"_id": insert_result.inserted_id})
    print("🧹 Test document deleted. All done!")

if __name__ == "__main__":
    asyncio.run(test_product_model_and_db())
