#!/usr/bin/env python3
"""
Script to check how seller_ids are stored in the products collection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.utils.database import db, users_collection
from bson import ObjectId

# Get the products collection
products_collection = db["products"]

print("Checking products in database...")
print("=" * 50)

# Get all products
products = list(products_collection.find({}))

if not products:
    print("No products found in database")
else:
    print(f"Found {len(products)} products:")
    print()
    
    for i, product in enumerate(products[:5]):  # Show first 5 products
        print(f"Product {i+1}:")
        print(f"  ID: {product.get('_id')}")
        print(f"  Name: {product.get('product_name')}")
        print(f"  Seller ID: {product.get('seller_id')} (type: {type(product.get('seller_id'))})")
        print(f"  Seller ID as string: {str(product.get('seller_id'))}")
        print()

print("=" * 50)
print("Check complete!") 