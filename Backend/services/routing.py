routing_map = {
    "Sanitation" : "Sanitation Department",
    "Electricity" : "Electricity Department",
    "Water Supply" : "Water Department",
    "Roads & Infrastructure" : "PWD Department",
}

def route_grievance(grievance_category):
    department = routing_map.get(grievance_category, " General Department")
    return department
