from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from Backend.utils.jwt_handler import get_current_user_id
from Backend.controllers.admin_controller import (
    get_all_sellers_controller,
    get_seller_detail_with_products,
    list_products_admin,
    update_product_admin,
    delete_product_admin,
    ban_seller_controller
)
from Backend.models.admin_model import (
    UserOutAdmin,
    UserDetailWithProducts,
    ProductOutAdmin,
    ProductUpdateAdmin,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/sellers", response_model=List[UserOutAdmin])
def admin_list_sellers(current_user_id: str = Depends(get_current_user_id)):
    return get_all_sellers_controller(current_user_id)

@router.get("/sellers/{seller_id}", response_model=UserDetailWithProducts)
def admin_get_seller_detail(current_user_id: str = Depends(get_current_user_id),
                            seller_id: str = None):
    return get_seller_detail_with_products(current_user_id, seller_id)

@router.get("/products", response_model=List[ProductOutAdmin])
def admin_list_products(
    current_user_id: str = Depends(get_current_user_id),
    search:    Optional[str] = Query(None, description="Search by name"),
    seller_id: Optional[str] = Query(None),
    status:    Optional[str] = Query(None),
    skip:      int            = Query(0),
    limit:     int            = Query(50),
):
    return list_products_admin(current_user_id, search, seller_id, status, skip, limit)

@router.patch("/products/{product_id}", response_model=ProductOutAdmin)
def admin_update_product(
    current_user_id: str     = Depends(get_current_user_id),
    product_id:      str     = None,
    update_in:       ProductUpdateAdmin = None
):
    return update_product_admin(current_user_id, product_id, update_in)

@router.delete("/products/{product_id}")
def admin_delete_product(current_user_id: str = Depends(get_current_user_id),
                         product_id: str = None):
    return delete_product_admin(current_user_id, product_id)

@router.post(
    "/sellers/{seller_id}/ban",
    summary="Admin Ban Seller",
    response_model=dict
)
def admin_ban_seller(
    seller_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Ban a seller by ID and deactivate all their products.
    """
    return ban_seller_controller(current_user_id, seller_id)