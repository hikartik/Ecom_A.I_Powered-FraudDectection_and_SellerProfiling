from fastapi import APIRouter, UploadFile, Form
from AI.Real_Time_Analysis.predict import run_prediction
from PIL import Image
from io import BytesIO

router = APIRouter()

@router.post("/")
async def predict(image: UploadFile, title: str = Form(...), desc: str = Form(...)):
    img = Image.open(BytesIO(await image.read())).convert("RGB")
    return run_prediction(img, title, desc)
