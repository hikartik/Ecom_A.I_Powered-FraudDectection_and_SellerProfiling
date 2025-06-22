from fastapi import HTTPException
from Backend.models.product_model import Product
from Backend.utils.database import db, users_collection
from Backend.utils.cloudinary_config import cloudinary
from datetime import datetime
from typing import List, Dict
from AI.Real_Time_Analysis.predict import run_prediction
from bson import ObjectId
from PIL import Image
from io import BytesIO
from fastapi import UploadFile
import random


product_collection = db["products"]

async def create_product_controller(
    seller_id: str,
    product_name: str,
    description: str,
    price: float,
    images: List[UploadFile]
) -> Dict:
    """
    Handle product creation: verify seller, run AI prediction,
    upload images to Cloudinary, insert into MongoDB,
    and return a JSON-safe response.
    """
    # 1) Verify user is a seller
    user = users_collection.find_one({"_id": ObjectId(seller_id)})
    if not user or user.get("user_type") != "seller":
        raise HTTPException(status_code=403, detail="Only sellers may add products")

    # 2) Read uploads into memory for both PIL and Cloudinary
    pil_images: List[Image.Image] = []
    raw_bytes: List[bytes] = []
    for img in images:
        content = await img.read()
        raw_bytes.append(content)
        try:
            pil_images.append(Image.open(BytesIO(content)))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

    # 3) Run AI prediction
    preds = run_prediction(pil_images, product_name, description)

    # 4) Upload to Cloudinary
    image_urls: List[str] = []
    for content in raw_bytes:
        buffer = BytesIO(content)
        buffer.name = "upload"
        try:
            resp = cloudinary.uploader.upload(buffer, folder="product_images")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Cloudinary upload failed: {e}")
        url = resp.get("secure_url")
        if not isinstance(url, str):
            raise HTTPException(status_code=500, detail="Invalid Cloudinary response")
        image_urls.append(url)
    _status = "blocked_ai" if preds.get("risk_label", "") == "High Risk" else "valid"

    # 5) Build Pydantic model with all fields including AI scores
    product = Product(
        seller_id=seller_id,
        product_name=product_name,
        description=description,
        price=price,
        images=image_urls,
        vision_score=preds.get("vision_score", 0.0),
        text_score=preds.get("text_score", 0.0),
        multimodal_score=preds.get("multimodal_score", 0.0),
        ensemble_score=preds.get("ensemble_score", random.uniform(0.5, 0.9)),
        risk_label=preds.get("risk_label", ""),
        status=_status,
        created_at=datetime.utcnow()
    )

    # 6) Serialize model to dict and format datetime
    data = product.model_dump()
    data["created_at"] = data["created_at"].isoformat()

    # 7) Insert into MongoDB and capture new ID
    result = product_collection.insert_one(data)
    data["id"] = str(result.inserted_id)
    # ensure no raw ObjectId remains
    data.pop("_id", None)

    # 8) Return JSON-safe response
    return {"message": "Product listed successfully", "product": data}

async def update_product_controller(
    product_id: str,
    seller_id: str,
    product_name: str,
    description: str,
    price: float
) -> Dict:
    """
    Handle product updates: verify seller owns the product,
    update fields, and return a JSON-safe response.
    """
    try:
        # 1) Verify user is a seller
        user = users_collection.find_one({"_id": ObjectId(seller_id)})
        if not user or user.get("user_type") != "seller":
            raise HTTPException(status_code=403, detail="Only sellers may update products")

        # 2) Verify the product exists and belongs to this seller
        product = product_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Convert both seller_ids to strings for comparison
        stored_seller_id = str(product.get("seller_id"))
        current_seller_id = str(seller_id)
        
        if stored_seller_id != current_seller_id:
            raise HTTPException(status_code=403, detail="You can only update your own products")

        # 3) Update the product
        update_data = {
            "product_name": product_name,
            "description": description,
            "price": price,
            "updated_at": datetime.utcnow()
        }

        result = product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update product")

        # 4) Get the updated product
        updated_product = product_collection.find_one({"_id": ObjectId(product_id)})
        
        # 5) Format the response
        response_data = {
            "id": str(updated_product["_id"]),
            "product_name": updated_product.get("product_name"),
            "description": updated_product.get("description"),
            "price": updated_product.get("price"),
            "images": updated_product.get("images", []),
            "status": updated_product.get("status", "valid"),
            "vision_score": updated_product.get("vision_score", 0.0),
            "text_score": updated_product.get("text_score", 0.0),
            "multimodal_score": updated_product.get("multimodal_score", 0.0),
            "ensemble_score": updated_product.get("ensemble_score", 0.0),
            "created_at": updated_product.get("created_at").isoformat() if hasattr(updated_product.get("created_at"), 'isoformat') else updated_product.get("created_at"),
            "updated_at": updated_product.get("updated_at").isoformat() if hasattr(updated_product.get("updated_at"), 'isoformat') else updated_product.get("updated_at")
        }

        return {"message": "Product updated successfully", "product": response_data}
    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
    except Exception as e:
        # Log the actual error and return a proper HTTP exception
        print(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def delete_product_controller(product_id: str, seller_id: str) -> Dict:
    """
    Handle product deletion: verify seller owns the product,
    delete it, and return a success response.
    """
    # 1) Verify user is a seller
    user = users_collection.find_one({"_id": ObjectId(seller_id)})
    if not user or user.get("user_type") != "seller":
        raise HTTPException(status_code=403, detail="Only sellers may delete products")

    # 2) Verify the product exists and belongs to this seller
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Convert both seller_ids to strings for comparison
    stored_seller_id = str(product.get("seller_id"))
    current_seller_id = str(seller_id)
    
    if stored_seller_id != current_seller_id:
        raise HTTPException(status_code=403, detail="You can only delete your own products")

    # 3) Delete the product
    result = product_collection.delete_one({"_id": ObjectId(product_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete product")

    return {"message": "Product deleted successfully"}

def get_products_by_seller(seller_id: str) -> List[Dict]:
    """
    Returns a list of products for the given seller_id,
    converting Mongo _id and datetimes to primitives.
    """
    cursor = product_collection.find({"seller_id": seller_id})
    products: List[Dict] = []
    for doc in cursor:
        created = doc.get("created_at")
        
        # Calculate average rating from reviews
        product_id = str(doc["_id"])
        reviews = list(db["reviews"].find({"product_id": product_id}))
        if reviews:
            total_rating = sum(review.get("rating", 0) for review in reviews)
            avg_rating = total_rating / len(reviews)
            avg_rating_rounded = round(avg_rating, 1)
            review_count = len(reviews)
        else:
            avg_rating_rounded = 3.0  # Default rating
            review_count = 0
        
        products.append({
            "id": product_id,
            "product_name": doc.get("product_name"),
            "description": doc.get("description"),
            "price": doc.get("price", 0.0),
            "images": doc.get("images", []),
            "status": doc.get("status", "valid"),
            "ensemble_score": doc.get("ensemble_score", 0.0),
            "avg_rating": avg_rating_rounded,
            "review_count": review_count,
            "created_at": (
                created.isoformat() if isinstance(created, datetime) else created
            )
        })
    return products

def get_all_products_controller() -> List[dict]:
    """
    Fetch every product from MongoDB and return a JSON‐serializable list.
    (synchronous)
    """
    try:
        docs = product_collection.find({})
        products = []
        for doc in docs:
            # Convert ObjectId to string
            doc["id"] = str(doc["_id"])
            doc.pop("_id", None)
            
            # Convert datetime to string if present
            if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
                doc["created_at"] = doc["created_at"].isoformat()
            
            # Calculate average rating from reviews
            product_id = doc["id"]
            reviews = list(db["reviews"].find({"product_id": product_id}))
            if reviews:
                total_rating = sum(review.get("rating", 0) for review in reviews)
                avg_rating = total_rating / len(reviews)
                doc["avg_rating"] = round(avg_rating, 1)
                doc["review_count"] = len(reviews)
            else:
                doc["avg_rating"] = 3.0  # Default rating
                doc["review_count"] = 0
            
            products.append(doc)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {e}")

def get_product_by_id_controller(product_id: str) -> dict:
    """
    Fetch a single product by ID from MongoDB and return a JSON‐serializable dict.
    """
    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=422, detail="Invalid product ID format")
        
        doc = product_collection.find_one({"_id": ObjectId(product_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Convert ObjectId to string
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        
        # Convert datetime to string if present
        if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
            doc["created_at"] = doc["created_at"].isoformat()
        
        # Calculate average rating from reviews
        reviews = list(db["reviews"].find({"product_id": product_id}))
        if reviews:
            total_rating = sum(review.get("rating", 0) for review in reviews)
            avg_rating = total_rating / len(reviews)
            doc["avg_rating"] = round(avg_rating, 1)
            doc["review_count"] = len(reviews)
        else:
            doc["avg_rating"] = 3.0  # Default rating
            doc["review_count"] = 0
        
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {e}")

    