import os
import requests

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine

from .controller.authentication import Authentication
from .controller.user import User
from .controller.security import create_access_token
from sqlalchemy.orm import Session, sessionmaker

from models.authModel import AuthBase
from models.userModel import UserBase

app = FastAPI()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
auth_service = Authentication()
user_service = User()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.post("/create_user", status_code=201)
async def create_user(data: UserBase, db: Session = Depends(get_db)):
    print(data)
    return user_service.create_user(data, db)

@app.post("/create_auth", status_code=201)
async def create_auth(credentials: AuthBase, db: Session = Depends(get_db)):
    return auth_service.create_auth(credentials, db)

@app.post("/login", status_code=200)
async def login(credentials: AuthBase, db: Session = Depends(get_db)):
    (user, auth) = auth_service.authenticate(credentials.email, credentials.password, db)

    access_token = create_access_token(
        data = {
            "email": auth.email, 
            "exp": datetime.utcnow() + timedelta(minutes=30)
        })
    
    return {
        "token_type": "bearer",
        "token": access_token
    }