from pydantic import BaseModel, Field,ValidationError
from typing import Optional
from datetime import datetime
from database import get_db
import asyncio

class Review(BaseModel):
    customer_id: str
    product_id: str
    seller_id: str
    comment: Optional[str] = None
    rating_score: int
    created_at: datetime = Field(default_factory=datetime.now)

   


async def test_review_model_and_db():
    db = get_db()
    reviews = db["review"]

    # (Optional) ensure an index on customer_id for fast lookups
    await reviews.create_index("customer_id")

    # 1) Test a valid review
    try:
        dummy = Review(
            customer_id="12323223932",
            product_id="12342556355434",
            seller_id="134243522435",
            comment="This product has been very helpful—it’s amazing!",
            rating_score=5,        # use a realistic score
        )
    except ValidationError as e:
        print("❌ Validation failed:", e)
        return

    print("✅ Generated Review model:")
    print(dummy.model_dump_json(indent=2))

    # 2) Insert into MongoDB
    data = dummy.model_dump()        # plain dict
    result = await reviews.insert_one(data)
    print(f"🆔 Inserted document with _id = {result.inserted_id!r}")

    # 3) Fetch & display
    fetched = await reviews.find_one({"_id": result.inserted_id})
    print("🔄 Fetched document from Mongo:")
    print(fetched)

    # 4) Cleanup
    await reviews.delete_one({"_id": result.inserted_id})
    print("🧹 Test document deleted. All done!")

if __name__ == "__main__":
    asyncio.run(test_review_model_and_db())