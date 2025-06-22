import sys
sys.path.append('.')
from utils.database import db

# Check admin users
admin_users = list(db['users'].find({'type': 'admin'}))
print(f'Admin users found: {len(admin_users)}')

for user in admin_users:
    print(f'ID: {user["_id"]}, Name: {user.get("name")}, Email: {user.get("email")}, Password Exists: {"password" in user}')

# Check for specific admin2@example.com
admin2 = db['users'].find_one({'email': 'admin2@example.com'})
if admin2:
    print(f'\nadmin2@example.com found!')
    print(f'ID: {admin2["_id"]}, Name: {admin2.get("name")}, Password Exists: {"password" in admin2}')
else:
    print('\nadmin2@example.com NOT found in database.')

# Check all users
all_users = list(db['users'].find({}))
print(f'\nAll users found: {len(all_users)}')

for user in all_users:
    print(f'ID: {user["_id"]}, Name: {user["name"]}, Email: {user["email"]}, Type: {user["type"]}') 