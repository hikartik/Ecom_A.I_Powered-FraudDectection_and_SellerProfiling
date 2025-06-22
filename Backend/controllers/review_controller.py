# controllers/review_controller.py
from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId
from Backend.utils.database import db
from Backend.models.review_model import ReviewCreate, Review

reviews_collection = db["reviews"]
products_collection = db["products"]
users_collection = db["users"]


def create_review_controller(product_id: str, review_in: ReviewCreate) -> Review:
    # validate product_id
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=422, detail="Invalid product_id format")
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # prevent seller reviewing own product
    if str(product.get("seller_id")) == review_in.customer_id:
        raise HTTPException(status_code=403, detail="Sellers cannot review their own product")

    # validate customer_id
    if not ObjectId.is_valid(review_in.customer_id):
        raise HTTPException(status_code=422, detail="Invalid customer_id format")
    customer = users_collection.find_one({"_id": ObjectId(review_in.customer_id)})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # prevent duplicate review
    exists = reviews_collection.find_one({
        "product_id": product_id,
        "customer_id": review_in.customer_id
    })
    if exists:
        raise HTTPException(status_code=400, detail="Customer has already reviewed this product")

    # prepare document with rating and default rating_score
    doc = {
        "customer_id": review_in.customer_id,
        "comment": review_in.comment,
        "rating": review_in.rating,
        "product_id": product_id,
        "seller_id": str(product.get("seller_id")),
        "rating_score": 0.0,
        "created_at": datetime.now()
    }
    result = reviews_collection.insert_one(doc)
    saved = reviews_collection.find_one({"_id": result.inserted_id})
    saved["_id"] = str(saved["_id"])
    return Review.model_validate(saved)


def get_reviews_for_product_controller(product_id: str) -> list[Review]:
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=422, detail="Invalid product_id format")
    cursor = reviews_collection.find({"product_id": product_id})
    reviews = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        reviews.append(Review.model_validate(doc))
    return reviews