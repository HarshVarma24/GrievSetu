from unicodedata import category
from ai_models.text_model import text_model
from services.routing import route_grievance
from services.priority import assign_priority
from services.sla import assign_sla
from ai_models.image_model import predict_image


# def process_grievance(text):
#     category, confidence = text_model(text)
#     department = route_grievance(category)
#     priority = assign_priority(text)
#     sla = assign_sla(priority)

#     return {
#         "input_text": text,
#         "predicted_category": category,
#         "confidence": round(float(confidence), 2),
#         "assigned_department": department,
#         "priority": priority,
#         "sla": sla
#     }

# result = process_grievance("Broken pipelines and loose electric wires on the street are causing both safety and infrastructure issues.")
# print(result)

def process_grievance(text="",img_path=""):
    category, text_confidence = text_model(text) if text else (None, 0)

    predicted_label, image_confidence = predict_image(img_path) if img_path else (None, 0)

    if text_confidence >= image_confidence:
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
