from fastapi import FastAPI
from models.user import GrievanceRequest, UserCreate, UserLogin
from models.grievance import Grievance
from models.schema import User
from database.database import engine, SessionLocal, Base
from fastapi import Depends, HTTPException
from auth.token import create_jwt, verify_jwt
from services.process import process_grievance
from fastapi import UploadFile, File
import os
import shutil
from sqlalchemy import func


app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

Base.metadata.create_all(bind=engine)

def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def test():
    return {"message": "Hello World"}

def admin_required(payload = Depends(verify_jwt), db: SessionLocal= Depends(get_db)):
    user = db.query(User).filter(User.email == payload["sub"]).first()
    
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user 
    
@app.post("/register")
def register(user: UserCreate, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
        
    new_user = User(
        name = user.name,
        email = user.email,
        password = user.password,
        role = "citizen"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}
    
@app.post("/login")
def login(user: UserLogin, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if not existing_user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    if existing_user.password != user.password:
        raise HTTPException(status_code = 401, detail = "Invalid password")
    
    return {"message": "User logged in successfully", 
            "token": create_jwt(user.email),
            "user_id" : existing_user.id,
            "role" : existing_user.role
        }
    
@app.get("/verifylogin")
def verify_login(payload = Depends(verify_jwt)):
    return {"message": "Token is valid", "payload": payload}


@app.post("/predict")
def predict_grievance(request: GrievanceRequest):
    result = process_grievance(
        text = request.text,
        img_path=request.img_path
    )
    return {
        "status": "success",
        "result": result
    }
    
@app.post("/submit")
def submit_grievance(request: GrievanceRequest):
    result = process_grievance(
        text = request.text,
        img_path = request.img_path,
        user_id = request.user_id
    )
    print("USER_ID :", request.user_id)
    return result

@app.get("/my_grievances/{user_id}")
def my_grievances(user_id: int, db: SessionLocal = Depends(get_db)):
    data = db.query(Grievance).filter(Grievance.user_id == user_id).all()
    return [
        {
            "id": grievance.id,
            "text": grievance.text,
            "category": grievance.category,
            "status": grievance.status,
            "priority": grievance.priority,
            "created_at": grievance.created_at
        }
        for grievance in data
    ]

@app.get("/dashboard/{user_id}")
def dashboard(user_id: int, db: SessionLocal = Depends(get_db)):

    total = db.query(Grievance).filter(Grievance.user_id == user_id).count()
    pending = db.query(Grievance).filter(Grievance.user_id == user_id, Grievance.status == "pending").count()
    resolved = db.query(Grievance).filter(Grievance.user_id == user_id, Grievance.status == "resolved").count()
    in_progress = db.query(Grievance).filter(Grievance.user_id == user_id, Grievance.status == "in_progress").count()

    return {
        "total": total,
        "pending": pending,
        "resolved": resolved,
        "in_progress": in_progress
    }

@app.get("/recent/{user_id}")
def recent(user_id: int, db: SessionLocal = Depends(get_db)):
    data = db.query(Grievance).filter(Grievance.user_id == user_id).order_by(Grievance.created_at.desc()).limit(5).all()
    return [
        {
            "id": grievance.id,
            "text": grievance.text,
            "category": grievance.category,
            "status": grievance.status,
        }
        for grievance in data
    ]

@app.get("/report/{user_id}")
def report(user_id: int, db: SessionLocal = Depends(get_db)):
    data = db.query(func.date(Grievance.created_at),func.count()).filter(Grievance.user_id == user_id).group_by(func.date(Grievance.created_at)).all()
    return [
        {
            "date": date,
            "count": count
        }
        for date, count in data
    ]

@app.get("/admin/all_grievances")
def all_grievances(admin = Depends(admin_required),db:SessionLocal = Depends(get_db)):
    data = db.query(Grievance).order_by(Grievance.created_at.desc()).all()
    return [
        {
            "id":grievance.id,
            "user_id":grievance.user_id,
            "text":grievance.text,
            "category":grievance.category,
            "status":grievance.status,
            "priority":grievance.priority,
            "created_at":grievance.created_at,
        }
        for grievance in data
    ]

@app.put("/admin/update_status/{id}")
def update_status(id: int, status: str, admin= Depends(admin_required), db: SessionLocal = Depends(get_db)):
    grievance = db.query(Grievance).filter(Grievance.id == id).first() 
    
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
        
    grievance.status = status
    db.commit()
    return {"message": "Status updated successfully"}
    
    
@app.put("/admin/update_priority/{id}")
def update_priority(id: int, priority: str, admin = Depends(admin_required), db: SessionLocal = Depends(get_db)):
    grievance = db.query(Grievance).filter(Grievance.id == id).first() 
    
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
        
    grievance.priority = priority
    db.commit()
    return {"message": "Priority updated successfully"}

@app.put("/admin/update_department/{id}")
def update_department(id: int, department: str, admin = Depends(admin_required), db: SessionLocal = Depends(get_db)):
    grievance = db.query(Grievance).filter(Grievance.id == id).first() 
    
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
        
    grievance.department = department
    db.commit()
    return {"message": "Department updated successfully"}

@app.get("/admin/filter/{status}")
def filter_status(status:str, admin = Depends(admin_required), db:SessionLocal = Depends(get_db)):
    data = db.query(Grievance).filter(Grievance.status == status).order_by(Grievance.created_at.desc()).all()
    return data