
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


product_collection = db["products"]

async def create_product_controller(
    seller_id: str,
    product_name: str,
    description: str,
    images: List[UploadFile]
) -> Dict:
    """
    Handle product creation: verify seller, run AI prediction,
    upload images to Cloudinary, insert into MongoDB,
    and return a JSON-safe response.
    """
    # 1) Verify user is a seller
    user = users_collection.find_one({"_id": ObjectId(seller_id)})
    if not user or user.get("type") != "seller":
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
        images=image_urls,
        vision_score=preds.get("vision_score", 0.0),
        text_score=preds.get("text_score", 0.0),
        multimodal_score=preds.get("multimodal_score", 0.0),
        ensemble_score=preds.get("ensemble_score", 0.0),
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
def get_products_by_seller(seller_id: str) -> List[Dict]:
    """
    Returns a list of products for the given seller_id,
    converting Mongo _id and datetimes to primitives.
    """
    cursor = product_collection.find({"seller_id": seller_id})
    products: List[Dict] = []
    for doc in cursor:
        created = doc.get("created_at")
        products.append({
            "id": str(doc["_id"]),
            "product_name": doc.get("product_name"),
            "description": doc.get("description"),
            "images": doc.get("images", []),
            "status": doc.get("status", "valid"),
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
        # normal for-loop, not async
        return [Product(**doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {e}")

    