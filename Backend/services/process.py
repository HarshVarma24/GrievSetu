from ai_models.text_model import text_model
from services.routing import route_grievance
from services.priority import assign_priority
from services.sla import assign_sla


def process_grievance(text):
    category, confidence = text_model(text)
    department = route_grievance(category)
    priority = assign_priority(text)
    sla = assign_sla(priority)

    return {
        "input_text": text,
        "predicted_category": category,
        "confidence": round(float(confidence), 2),
        "assigned_department": department,
        "priority": priority,
        "sla": sla
    }

result = process_grievance("Broken pipelines and loose electric wires on the street are causing both safety and infrastructure issues.")
print(result)
