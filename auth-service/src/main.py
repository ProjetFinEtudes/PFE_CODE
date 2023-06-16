import os
import requests

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine

from .controller import authentication as auth_controller
from .controller.security import create_access_token
from sqlalchemy.orm import Session, sessionmaker

from models.authModel import AuthBase, Auth
from models.userModel import UserBase

app = FastAPI()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.post("/", status_code=201)
async def create_auth(credentials: AuthBase, db: Session = Depends(get_db)):
    return auth_controller.create_auth(credentials, db)

@app.get("/")
def get_auth(id_auth: int, db: Session = Depends(get_db)):
    return auth_controller.get_auth_by_id(id_auth, db)

@app.patch("/")
def update_auth(auth: Auth, db: Session = Depends(get_db)):
    return auth_controller.update_auth(auth, db)


@app.delete("/")
def delete_auth(id_auth: int, db: Session = Depends(get_db)):
    return auth_controller.delete_auth_by_id(id_auth, db)

@app.post("/login", status_code=200)
async def login(credentials: AuthBase, db: Session = Depends(get_db)):
    (user, auth) = auth_controller.authenticate(credentials, db)

    access_token = create_access_token(
        data = {
            "email": auth.email, 
            "exp": datetime.utcnow() + timedelta(minutes=30)
        })
    
    return {
        "token_type": "bearer",
        "token": access_token
    }