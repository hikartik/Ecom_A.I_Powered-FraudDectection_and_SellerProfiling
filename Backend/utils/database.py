# utils/database.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[MONGO_DB]
users_collection = db["users"]

def connect_to_mongo():
    try:
        client.admin.command("ping")
        print("✅ MongoDB Atlas connection established!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise
