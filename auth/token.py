import jwt 
from fastapi import HTTPException, Depends, Header
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_jwt(name: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "name":name,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return token
    
def verify_jwt(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code = 401, detail = "Authorization token is missing")
    
    try:
        token = Authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Invalid token")

