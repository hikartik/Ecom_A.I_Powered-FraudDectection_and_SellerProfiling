import os
from PIL import Image
from predict_helper import run_prediction

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "./../.."))
IMAGE_DIR = os.path.join(BASE_DIR, "gallery_images")

# Load sample images
image_paths = [
    os.path.join(IMAGE_DIR, "Samsung_galaxy_s21_ultra_1.jpg"),
    os.path.join(IMAGE_DIR, "Samsung_galaxy_s21_ultra_2.jpg")
]

images = [Image.open(path).convert("RGB") for path in image_paths]

# Sample title and description
title = "Stylish T-Shirt"
desc = "A comfortable and trendy cotton t-shirt suitable for all seasons."

# Run prediction
result = run_prediction(images, title, desc)

# Print the results
print("🔍 Prediction Output:")
for key, value in result.items():
    print(f"{key}: {value}")
