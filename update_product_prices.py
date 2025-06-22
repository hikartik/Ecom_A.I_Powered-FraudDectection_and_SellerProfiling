#!/usr/bin/env python3
"""
Script to update existing products with price fields
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.utils.database import db
from bson import ObjectId

# Get the products collection
product_collection = db["products"]

# Price mapping for existing products
price_mapping = {
    "Samsung Galaxy S24 Ultra": 129999.00,
    "Apple iPhone 15 Pro Max": 149999.00,
    "Suspicious Electronic Device": 2999.00,
    "Gaming Laptop RTX 4080": 189999.00,
    "Wireless Bluetooth Headphones": 24999.00
}

def update_product_prices():
    """Update existing products with price fields"""
    try:
        # Get all products that don't have a price field
        products_without_price = product_collection.find({"price": {"$exists": False}})
        
        updated_count = 0
        for product in products_without_price:
            product_name = product.get("product_name", "")
            
            # Set default price if not in mapping
            price = price_mapping.get(product_name, 9999.00)
            
            # Update the product with price
            result = product_collection.update_one(
                {"_id": product["_id"]},
                {"$set": {"price": price}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"Updated {product_name} with price: ₹{price:,.2f}")
        
        print(f"\nSuccessfully updated {updated_count} products with price fields.")
        
        # Show all products with their prices
        print("\nCurrent products in database:")
        all_products = product_collection.find()
        for product in all_products:
            price = product.get("price", "No price set")
            print(f"- {product.get('product_name', 'Unknown')}: ₹{price:,.2f}" if isinstance(price, (int, float)) else f"- {product.get('product_name', 'Unknown')}: {price}")
            
    except Exception as e:
        print(f"Error updating product prices: {e}")

if __name__ == "__main__":
    update_product_prices() 