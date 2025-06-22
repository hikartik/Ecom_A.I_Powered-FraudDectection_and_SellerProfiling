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
from Backend.controllers.batch_review_controller import batch_update_review_scores
from Backend.controllers.batch_seller_controller import batch_update_seller_scores
from Backend.utils.scheduler import scheduler

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

@router.post("/trigger-review-update")
async def trigger_review_update():
    """Manually trigger batch review score update"""
    try:
        result = await batch_update_review_scores()
        return {"success": True, "message": "Review scores updated successfully", "result": result}
    except Exception as e:
        return {"success": False, "message": f"Error updating review scores: {str(e)}"}

@router.post("/trigger-seller-update")
async def trigger_seller_update():
    """Manually trigger batch seller score update"""
    try:
        result = await batch_update_seller_scores()
        return {"success": True, "message": "Seller scores updated successfully", "result": result}
    except Exception as e:
        return {"success": False, "message": f"Error updating seller scores: {str(e)}"}

@router.post("/trigger-all-updates")
async def trigger_all_updates():
    """Manually trigger both review and seller score updates"""
    try:
        review_result = await batch_update_review_scores()
        seller_result = await batch_update_seller_scores()
        return {
            "success": True, 
            "message": "All scores updated successfully", 
            "review_result": review_result,
            "seller_result": seller_result
        }
    except Exception as e:
        return {"success": False, "message": f"Error updating scores: {str(e)}"}

@router.get("/scheduler-status")
async def get_scheduler_status():
    """Get the current status of the scheduler"""
    try:
        jobs = []
        for job in scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time) if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        
        return {
            "success": True,
            "scheduler_running": scheduler.running,
            "jobs": jobs,
            "job_count": len(jobs)
        }
    except Exception as e:
        return {"success": False, "message": f"Error getting scheduler status: {str(e)}"}