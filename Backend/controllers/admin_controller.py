from fastapi import HTTPException, status
from bson import ObjectId
from Backend.utils.database import db
from Backend.models.admin_model import (
    UserOutAdmin,
    ProductOutAdmin,
    ProductUpdateAdmin,
    UserDetailWithProducts,
)

users_col    = db["users"]
products_col = db["products"]
reviews_col  = db["reviews"]

def check_admin_role(current_user_id: str):
    if not ObjectId.is_valid(current_user_id):
        raise HTTPException(422, "Invalid user_id format")
    user = users_col.find_one({"_id": ObjectId(current_user_id)})
    if not user or user.get("type") != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin access required")
    return user

def get_all_sellers_controller(current_user_id: str):
    check_admin_role(current_user_id)
    out = []
    for doc in users_col.find({"type": "seller"}):
        out.append(UserOutAdmin(
            id=str(doc["_id"]),
            name=doc["name"],
            email=doc["email"],
            type=doc["type"],
            score=doc.get("score", 0.0),
            created_at=doc.get("created_at"),
            is_banned=doc.get("is_banned", False),
        ))
    return out

def get_seller_detail_with_products(current_user_id: str, seller_id: str):
    check_admin_role(current_user_id)
    if not ObjectId.is_valid(seller_id):
        raise HTTPException(422, "Invalid seller_id format")
    user = users_col.find_one({"_id": ObjectId(seller_id)})
    if not user or user.get("type") != "seller":
        raise HTTPException(404, "Seller not found")

    user_out = UserOutAdmin(
        id=seller_id,
        name=user["name"],
        email=user["email"],
        type=user["type"],
        score=user.get("score", 0.0),
        created_at=user.get("created_at"),
        is_banned=user.get("is_banned", False),
    )

    prods = []
    for p in products_col.find({"seller_id": seller_id, "status": "valid"}):
        p["_id"] = str(p["_id"])
        prods.append(ProductOutAdmin.model_validate(p))

    return UserDetailWithProducts(user=user_out, products=prods)

def list_products_admin(current_user_id: str,
                        search: str = None,
                        seller_id: str = None,
                        status: str = None,
                        skip: int = 0,
                        limit: int = 50):
    check_admin_role(current_user_id)
    q = {}
    if search:
        q["product_name"] = {"$regex": search, "$options": "i"}
    if seller_id:
        q["seller_id"] = seller_id
    if status:
        q["status"] = status

    out = []
    cursor = products_col.find(q).skip(skip).limit(limit)
    for p in cursor:
        p["_id"] = str(p["_id"])
        out.append(ProductOutAdmin.model_validate(p))
    return out

def update_product_admin(current_user_id: str,
                         product_id: str,
                         update_in: ProductUpdateAdmin):
    check_admin_role(current_user_id)
    if not ObjectId.is_valid(product_id):
        raise HTTPException(422, "Invalid product_id format")
    p = products_col.find_one({"_id": ObjectId(product_id)})
    if not p:
        raise HTTPException(404, "Product not found")

    upd = {}
    if update_in.ensemble_score is not None:
        upd["ensemble_score"] = update_in.ensemble_score
    if update_in.status is not None:
        upd["status"] = update_in.status
    if upd:
        products_col.update_one({"_id": ObjectId(product_id)}, {"$set": upd})

    p = products_col.find_one({"_id": ObjectId(product_id)})
    p["_id"] = str(p["_id"])
    return ProductOutAdmin.model_validate(p)

def delete_product_admin(current_user_id: str, product_id: str):
    check_admin_role(current_user_id)
    if not ObjectId.is_valid(product_id):
        raise HTTPException(422, "Invalid product_id format")
    res = products_col.delete_one({"_id": ObjectId(product_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Product not found")
    reviews_col.delete_many({"product_id": product_id})
    return {"detail": f"Product {product_id} deleted"}


from fastapi import HTTPException, status
from bson import ObjectId
from Backend.utils.database import db

users_col    = db["users"]
products_col = db["products"]

def ban_seller_controller(current_user_id: str, seller_id: str):
    # ensure caller is admin
    from .admin_controller import check_admin_role
    check_admin_role(current_user_id)

    # validate seller_id
    if not ObjectId.is_valid(seller_id):
        raise HTTPException(status_code=422, detail="Invalid seller_id format")

    seller = users_col.find_one({"_id": ObjectId(seller_id)})
    if not seller or seller.get("type") != "seller":
        raise HTTPException(status_code=404, detail="Seller not found")

    # ban the seller
    users_col.update_one(
        {"_id": ObjectId(seller_id)},
        {"$set": {"is_banned": True}}
    )
    # deactivate all their products
    products_col.update_many(
        {"seller_id": seller_id},
        {"$set": {"status": "blocked_batch"}}
    )

    return {"detail": f"Seller {seller_id} banned and their products deactivated"}