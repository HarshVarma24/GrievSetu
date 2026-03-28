def assign_priority(text):
    text = text.lower()
    if "emergency" in text or "urgent" in text or "immediate" in text or "danger" in text or "hazard" in text:
        return "High"
    elif "important" in text or  "soon" in text or "asap" in text or "priority" in text:
        return "Medium"
    else:
        return "Low"
