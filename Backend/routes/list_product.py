# backend/routes/list_product.py

from fastapi import APIRouter, UploadFile, Form
from Backend.utils.predict_helper import run_prediction
from PIL import Image
from io import BytesIO

router = APIRouter()

@router.post("/")
async def list_product(image: UploadFile, title: str = Form(...), desc: str = Form(...)):
    img = Image.open(BytesIO(await image.read())).convert("RGB")
    result = run_prediction(image, title, desc)

    # Optional: Add listing save logic here

    result["message"] = "Listing received and analyzed."
    return result
