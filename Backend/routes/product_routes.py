from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import List
from Backend.controllers.product_controller import (
    create_product_controller,
    get_products_by_seller,
    get_all_products_controller,
    update_product_controller,
    delete_product_controller
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
    price: float = Form(...),
    images: List[UploadFile] = File(...),
    seller_id: str = Depends(get_current_user_id),
):
    return await create_product_controller(
        product_name=product_name,
        description=description,
        price=price,
        images=images,
        seller_id=seller_id
    )

# Seller route to get all of *their* products
@router.get("/my")
def list_my_products(seller_id: str = Depends(get_current_user_id)):
    return get_products_by_seller(seller_id)

# Get items for user dashboard
@router.get("/api/", summary="List all products")
def list_all_products():
    # you can keep this sync too
    return get_all_products_controller()

# Add product via API endpoint
@router.post("/api/")
async def add_product_api(
    product_name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(None),
    seller_id: str = Depends(get_current_user_id),
):
    images = [image] if image else []
    return await create_product_controller(
        product_name=product_name,
        description=description,
        price=price,
        images=images,
        seller_id=seller_id
    )

# Update product via API endpoint
@router.put("/api/{product_id}")
async def update_product_api(
    product_id: str,
    product_name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    seller_id: str = Depends(get_current_user_id),
):
    return await update_product_controller(
        product_id=product_id,
        product_name=product_name,
        description=description,
        price=price,
        seller_id=seller_id
    )

# Delete product via API endpoint
@router.delete("/api/{product_id}")
async def delete_product_api(
    product_id: str,
    seller_id: str = Depends(get_current_user_id),
):
    return await delete_product_controller(
        product_id=product_id,
        seller_id=seller_id
    )

