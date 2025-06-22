#!/usr/bin/env python3
"""
Script to add demo users to the database for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.utils.database import db, users_collection
from datetime import datetime
from passlib.context import CryptContext

# Get the users collection
users_collection = db["users"]

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Demo users data
demo_users = [
    {
        "full_name": "Demo Customer",
        "email": "customer@demo.com",
        "phone": "+1234567890",
        "password": pwd_context.hash("password123"),
        "user_type": "user",
        "created_at": datetime.utcnow()
    },
    {
        "full_name": "Demo Seller",
        "email": "seller@demo.com",
        "phone": "+1234567891",
        "password": pwd_context.hash("password123"),
        "user_type": "seller",
        "created_at": datetime.utcnow()
    },
    {
        "full_name": "Demo Admin",
        "email": "admin@demo.com",
        "phone": "+1234567892",
        "password": pwd_context.hash("password123"),
        "user_type": "admin",
        "created_at": datetime.utcnow()
    }
]

def add_demo_users():
    """Add demo users to the database"""
    try:
        # Check if demo users already exist
        existing_count = users_collection.count_documents({"email": {"$in": [user["email"] for user in demo_users]}})
        if existing_count > 0:
            print(f"Demo users already exist in database. Skipping demo user creation.")
            return
        
        # Insert demo users
        result = users_collection.insert_many(demo_users)
        print(f"Successfully added {len(result.inserted_ids)} demo users to the database.")
        
        # Display the added users
        for user in demo_users:
            print(f"- {user['full_name']} ({user['email']}) - Type: {user['user_type']}")
            
        print("\nDemo Login Credentials:")
        print("Customer: customer@demo.com / password123")
        print("Seller: seller@demo.com / password123")
        print("Admin: admin@demo.com / password123")
            
    except Exception as e:
        print(f"Error adding demo users: {e}")

if __name__ == "__main__":
    add_demo_users() 