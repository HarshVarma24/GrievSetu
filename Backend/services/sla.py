SLA_RULES = {
    "High" : "24hours",
    "Medium" : "48hours",
    "Low" : "72hours"
}

def assign_sla(priority):
    return SLA_RULES.get(priority, "72hours")
