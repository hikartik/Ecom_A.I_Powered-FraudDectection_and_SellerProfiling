#!/usr/bin/env python3
"""
Script to add sample products to the database for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.utils.database import db
from datetime import datetime
from bson import ObjectId

# Get the products collection
product_collection = db["products"]

# Sample products data
sample_products = [
    {
        "seller_id": "507f1f77bcf86cd799439011",  # Sample seller ID
        "product_name": "Samsung Galaxy S24 Ultra",
        "description": "Latest flagship smartphone with advanced AI features and premium camera system",
        "price": 129999.00,
        "images": ["https://example.com/samsung1.jpg"],
        "vision_score": 0.85,
        "text_score": 0.92,
        "multimodal_score": 0.88,
        "ensemble_score": 0.88,
        "risk_label": "Low Risk",
        "batch_score": 0.90,
        "status": "valid",
        "created_at": datetime.utcnow()
    },
    {
        "seller_id": "507f1f77bcf86cd799439011",
        "product_name": "Apple iPhone 15 Pro Max",
        "description": "Premium iPhone with titanium design and professional camera capabilities",
        "price": 149999.00,
        "images": ["https://example.com/iphone1.jpg"],
        "vision_score": 0.78,
        "text_score": 0.85,
        "multimodal_score": 0.82,
        "ensemble_score": 0.82,
        "risk_label": "Low Risk",
        "batch_score": 0.88,
        "status": "valid",
        "created_at": datetime.utcnow()
    },
    {
        "seller_id": "507f1f77bcf86cd799439011",
        "product_name": "Suspicious Electronic Device",
        "description": "Generic electronic device with unclear specifications",
        "price": 2999.00,
        "images": ["https://example.com/suspicious1.jpg"],
        "vision_score": 0.45,
        "text_score": 0.32,
        "multimodal_score": 0.38,
        "ensemble_score": 0.38,
        "risk_label": "High Risk",
        "batch_score": 0.25,
        "status": "blocked_ai",
        "created_at": datetime.utcnow()
    },
    {
        "seller_id": "507f1f77bcf86cd799439011",
        "product_name": "Gaming Laptop RTX 4080",
        "description": "High-performance gaming laptop with RTX 4080 graphics card",
        "price": 189999.00,
        "images": ["https://example.com/laptop1.jpg"],
        "vision_score": 0.92,
        "text_score": 0.89,
        "multimodal_score": 0.91,
        "ensemble_score": 0.91,
        "risk_label": "Low Risk",
        "batch_score": 0.95,
        "status": "valid",
        "created_at": datetime.utcnow()
    },
    {
        "seller_id": "507f1f77bcf86cd799439011",
        "product_name": "Wireless Bluetooth Headphones",
        "description": "Premium noise-cancelling wireless headphones with long battery life",
        "price": 24999.00,
        "images": ["https://example.com/headphones1.jpg"],
        "vision_score": 0.88,
        "text_score": 0.91,
        "multimodal_score": 0.89,
        "ensemble_score": 0.89,
        "risk_label": "Low Risk",
        "batch_score": 0.92,
        "status": "valid",
        "created_at": datetime.utcnow()
    }
]

def add_sample_products():
    """Add sample products to the database"""
    try:
        # Check if products already exist
        existing_count = product_collection.count_documents({})
        if existing_count > 0:
            print(f"Database already contains {existing_count} products. Skipping sample data addition.")
            return
        
        # Insert sample products
        result = product_collection.insert_many(sample_products)
        print(f"Successfully added {len(result.inserted_ids)} sample products to the database.")
        
        # Display the added products
        for product in sample_products:
            print(f"- {product['product_name']} (AI Score: {product['ensemble_score']:.2f}, Status: {product['status']})")
            
    except Exception as e:
        print(f"Error adding sample products: {e}")

if __name__ == "__main__":
    add_sample_products() 