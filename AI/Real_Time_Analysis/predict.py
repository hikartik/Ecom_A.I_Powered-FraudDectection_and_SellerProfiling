from PIL import Image

from AI.Real_Time_Analysis import vision_model, text_model, multimodal_model
from AI.Real_Time_Analysis.ensemble import ensemble_score

def run_prediction(images: list[Image.Image], title: str, desc: str):
    v_score = vision_model.predict(images)
    m_score = multimodal_model.predict(images, title, desc)
    t_score = text_model.predict(title, desc)

    final_score, label = ensemble_score(v_score, t_score, m_score)

    return {
        "vision_score": v_score,
        "text_score": t_score,
        "multimodal_score": m_score,
        "ensemble_score": final_score,
        "risk_label": label
    }
