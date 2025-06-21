from fastapi import HTTPException
from Backend.models.product_model import Product
from Backend.utils.database import db
from Backend.utils.cloudinary_config import cloudinary
from datetime import datetime
from typing import List, Dict

product_collection = db["products"]

async def create_product_controller(
    seller_id: str,
    product_name: str,
    description: str,
    images
) -> dict:
    """
    Handle product creation: upload images, validate data,
    insert into MongoDB, and return a JSON-safe response.
    """
    image_urls: List[str] = []
    for image in images:
        try:
            upload = cloudinary.uploader.upload(
                image.file,
                folder="product_images"
            )
        except Exception as e:
            # Surface Cloudinary error as HTTPException
            raise HTTPException(status_code=400, detail=f"Cloudinary upload failed: {e}")
        image_urls.append(upload["secure_url"])

    # Build and validate product with Pydantic
    product = Product(
        seller_id=seller_id,
        product_name=product_name,
        description=description,
        images=image_urls,
        created_at=datetime.utcnow()
    )

    # Dump to plain dict and serialize datetime
    data = product.model_dump()
    data["created_at"] = data["created_at"].isoformat()

    # Insert into MongoDB
    result = product_collection.insert_one(data)

    # Add stringified ID and clean up
    data["id"] = str(result.inserted_id)
    data.pop("_id", None)

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
