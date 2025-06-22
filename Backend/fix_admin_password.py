from utils.database import db
from passlib.hash import bcrypt

admin_email = "admin1@example.com"
new_password = "admin123"

hashed = bcrypt.hash(new_password)
result = db['users'].update_one(
    {"email": admin_email},
    {"$set": {"password": hashed}}
)
print("Updated admin password:", result.modified_count) 