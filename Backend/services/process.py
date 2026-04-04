from ai_models.text_model import text_model
from services.routing import route_grievance
from services.priority import assign_priority
from services.sla import assign_sla
from ai_models.image_model import predict_image

#NORMALIZE MAP 
NORMALIZE_MAP = {
    "water": "Water Supply",
    "water supply": "Water Supply",
    "road": "Roads & Infrastructure",
    "road & infra": "Roads & Infrastructure",
    "roads": "Roads & Infrastructure",
    "roads & infrastructure": "Roads & Infrastructure",
    "sanitation": "Sanitation",
    "electricity": "Electricity"
}


def process_grievance(text="",img_path=""):
    category, text_confidence = text_model(text) if text else (None, 0)
    predicted_label, image_confidence = predict_image(img_path) if img_path else (None, 0)

    text_confidence = float(text_confidence)
    image_confidence = float(image_confidence)

    norm_text = NORMALIZE_MAP.get(category.lower().strip(), category.strip()) if category else None
    norm_image = NORMALIZE_MAP.get(predicted_label.lower().strip(), predicted_label.strip()) if predicted_label else None
    
    print("RAW:", category, predicted_label)
    print("NORMALIZED:", norm_text, norm_image)

    CONF_THRESHOLD = 0.8
    if norm_text and norm_image:
        if norm_text != norm_image:
            if text_confidence > CONF_THRESHOLD and image_confidence > CONF_THRESHOLD:
                return{
                    "status": "Blocked",
                    "reason": "Conflicting predictions with high confidence. Requires manual review.",
                    "text_prediction": {"category": category, "confidence": text_confidence},
                    "image_prediction": {"category": predicted_label, "confidence": image_confidence}
                }
    

    TEXT_WEIGHT = 0.6
    IMAGE_WEIGHT = 0.4

    text_score = text_confidence * TEXT_WEIGHT
    image_score = image_confidence * IMAGE_WEIGHT

    if text_score >= image_score:
        final_category = category
        confidence = text_confidence
    else:
        final_category = predicted_label
        confidence = image_confidence

    department = route_grievance(final_category)
    priority = assign_priority(text)
    sla = assign_sla(priority)

    return {
        "input_text": text,
        "input_image": img_path,
        "predicted_category": final_category,
        "confidence": round(float(confidence), 2),
        "assigned_department": department,
        "priority": priority,
        "sla": sla
   }
