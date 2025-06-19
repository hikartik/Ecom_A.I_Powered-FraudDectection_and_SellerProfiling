def ensemble_score(vision_score, text_score, multimodal_score, weights=(0.4, 0.3, 0.3)):
    score = vision_score * weights[0] + text_score * weights[1] + multimodal_score * weights[2]
    label = "Low Risk" if score > 0.5 else "High Risk"
    return score, label
