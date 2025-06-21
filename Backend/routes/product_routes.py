from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import List

from Backend.controllers.product_controller import (
    create_product_controller,
    get_products_by_seller
)
from Backend.utils.jwt_handler import get_current_user_id

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Seller route to add product (seller_id from JWT)
@router.post("/add")
async def add_product(
    product_name: str = Form(...),
    description: str = Form(""),
    images: List[UploadFile] = File(...),
    seller_id: str = Depends(get_current_user_id),
):
    return await create_product_controller(
        seller_id=seller_id,
        product_name=product_name,
        description=description,
        images=images
    )

# Seller route to get all of *their* products
@router.get("/my")
def list_my_products(seller_id: str = Depends(get_current_user_id)):
    return get_products_by_seller(seller_id)
