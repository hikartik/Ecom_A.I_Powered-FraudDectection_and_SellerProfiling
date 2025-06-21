def dynamic_weights(vision, text, multi):
    # Confidence = how far score is from 0.5 (uncertainty)
    confs = [abs(vision - 0.5), abs(text - 0.5), abs(multi - 0.5)]
    total = sum(confs)
    if total == 0:
        return [1/3, 1/3, 1/3]  # fallback if all uncertain
    return [c / total for c in confs]

def classify_risk(score):
    if score < 0.5:
        return "High Risk"
    elif score < 0.75:
        return "Moderate Risk"
    else:
        return "Low Risk"

def ensemble_score(vision_score, text_score, multimodal_score):
    w1, w2, w3 = dynamic_weights(vision_score, text_score, multimodal_score)
    final_score = vision_score * w1 + text_score * w2 + multimodal_score * w3
    risk_label = classify_risk(final_score)

    return final_score, risk_label
