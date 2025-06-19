from PIL import Image
from AI import vision_model, text_model, multimodal_model
from AI.ensemble import ensemble_score

def run_prediction(image: Image.Image, title: str, desc: str):
    v_score = vision_model.predict(image)
    t_score = text_model.predict(f"{title}. {desc}")
    m_score = multimodal_model.predict(image, title, desc)
    final_score, label = ensemble_score(v_score, t_score, m_score)
    
    return {
        "vision_score": v_score,
        "text_score": t_score,
        "multimodal_score": m_score,
        "ensemble_score": final_score,
        "risk_label": label
    }
