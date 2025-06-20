from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from uuid import uuid4
from datetime import datetime
import asyncio

# 1) Pydantic v2‐style model
class User(BaseModel):
    name: str
    type: Literal["seller", "admin", "customer"]
    email: EmailStr
    score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)


    # No Config block needed for this simple use case



# 2) Mongo setup

from database import db  # assumes you're running from the backend/ folder
users = db["users"]

async def init_indexes():
    await users.create_index("email", unique=True)

# 3) Standalone test
if __name__ == "__main__":
    async def _test():
        print("🔎 Testing User model and MongoDB…")
        await init_indexes()

        # Create and print a dummy user
        dummy = User(
            name="Test Seller",
            type="seller",
            email="test.seller@example.com"
        )
        print("Generated User model:")
        print(dummy.model_dump_json(indent=2))

        # Insert into MongoDB
        data = dummy.model_dump()  # plain dict
        result = await users.insert_one(data)
        print(f"Inserted user with _id = {result.inserted_id}")

        # Fetch & display
        fetched = await users.find_one({"_id": result.inserted_id})
        print("Fetched document:", fetched)

        # Cleanup
        #await users.delete_one({"_id": result.inserted_id})
        #print("🧹 Test user deleted. Done.")

    asyncio.run(_test())
