import sys
sys.path.append('.')
from utils.database import db
from passlib.hash import bcrypt
from datetime import datetime
from bson import ObjectId

# Create new admin user
admin_data = {
    "email": "admin2@example.com",
    "password": bcrypt.hash("12345678"),
    "name": "Admin2",
    "type": "admin",
    "created_at": datetime.utcnow()
}

# Check if admin already exists
existing_admin = db['users'].find_one({"email": "admin2@example.com"})
if existing_admin:
    print("Admin2 already exists, updating password and name...")
    result = db['users'].update_one(
        {"email": "admin2@example.com"},
        {"$set": {
            "password": admin_data["password"],
            "name": admin_data["name"],
            "type": "admin"
        }}
    )
    print(f"Updated admin2: {result.modified_count} records modified")
else:
    print("Creating new admin2 user...")
    result = db['users'].insert_one(admin_data)
    print(f"Created admin2 with ID: {result.inserted_id}")

# Verify the admin was created/updated
admin = db['users'].find_one({"email": "admin2@example.com"})
print(f"\nVerification:")
print(f"Email: {admin['email']}")
print(f"Name: {admin.get('name', 'N/A')}")
print(f"Type: {admin.get('type', 'N/A')}")
print(f"Password exists: {'password' in admin}")
print(f"ID: {admin['_id']}") 