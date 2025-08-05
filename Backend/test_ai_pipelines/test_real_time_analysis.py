import os
import sys
from PIL import Image

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "./../.."))
sys.path.insert(0, project_root)

from AI.Real_Time_Analysis.predict import run_prediction

IMAGE_DIR = os.path.join(project_root, "gallery_images")


def load_images():
    paths = [
        os.path.join(IMAGE_DIR, "Samsung_galaxy_s21_ultra_1.jpg"),
        os.path.join(IMAGE_DIR, "Samsung_galaxy_s21_ultra_2.jpg"),
    ]
    return [Image.open(path).convert("RGB") for path in paths]


def test_run_prediction():
    images = load_images()
    title = "Stylish T-Shirt"
    desc = "A comfortable and trendy cotton t-shirt suitable for all seasons."

    result = run_prediction(images, title, desc)
    expected_keys = {
        "vision_score",
        "text_score",
        "multimodal_score",
        "ensemble_score",
        "risk_label",
    }

    assert set(result.keys()) == expected_keys
    for key in ["vision_score", "text_score", "multimodal_score", "ensemble_score"]:
        assert 0.0 <= result[key] <= 1.0
    assert result["risk_label"] in {"High Risk", "Moderate Risk", "Low Risk"}
