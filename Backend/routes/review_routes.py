# routes/review_routes.py
from fastapi import APIRouter
from typing import List
from Backend.models.review_model import ReviewCreate, Review
from Backend.controllers.review_controller import (
    create_review_controller,
    get_reviews_for_product_controller,
)

router = APIRouter(
    prefix="/products/{product_id}/reviews",
    tags=["Reviews"]
)

@router.post("/", response_model=Review, summary="Post a review for a product")
def post_review(product_id: str, review: ReviewCreate):
    return create_review_controller(product_id, review)

@router.get("/", response_model=List[Review], summary="Get all reviews for a product")
def list_reviews(product_id: str):
    return get_reviews_for_product_controller(product_id)
