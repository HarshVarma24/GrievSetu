from fastapi import FastAPI
from models.user import UserCreate, UserLogin
from models.models import User
from database.database import engine, SessionLocal, Base
from fastapi import Depends, HTTPException

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def test():
    return {"message": "Hello World"}
    
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
    existing_user = db.query(User).filter(User.name == user.name).first()
    
    if not existing_user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    if existing_user.password != user.password:
        raise HTTPException(status_code = 401, detail = "Invalid password")
    
    return {"message": "User logged in successfully"}

    

