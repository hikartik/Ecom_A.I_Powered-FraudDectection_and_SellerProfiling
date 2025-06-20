# app/database.py

import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

# 1) Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()   # <-- this reads .env into os.environ

logger = logging.getLogger(__name__)

# 2) Now these will not be None (assuming your .env has these entries):
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB  = os.getenv("MONGO_DB",  "trust_safety")

# 3) Initialize MongoDB client with a connection timeout
_client: AsyncIOMotorClient = AsyncIOMotorClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# 4) Reference the specific database
db = _client[MONGO_DB]

async def connect_to_mongo():
    """Verify the Mongo connection on startup."""
    try:
        await _client.admin.command("ping")
        print("✅ Successfully connected to MongoDB")
    except ServerSelectionTimeoutError as err:
        print(f"❌ Could not connect to MongoDB: {err}")
        raise

async def close_mongo_connection():
    """Cleanly close the Mongo client on shutdown."""
    _client.close()
    print("🔒 MongoDB connection closed")

def get_db():
    """FastAPI dependency to retrieve the DB instance."""
    return db



if __name__ == "__main__":
    # Standalone test: ping Mongo then exit
    import asyncio
    async def _test():
        try:
            await connect_to_mongo()
        finally:
            await close_mongo_connection()
    asyncio.run(_test())
