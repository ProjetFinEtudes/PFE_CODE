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

# créer model userauth

@app.post("/create_user", status_code=201)
async def create_user(data: UserBase, db: Session = Depends(get_db)):
    return user_service.create_user(data, db)

@app.post("/create_auth")
async def create_auth(credentials: AuthBase, db: Session = Depends(get_db)):
    return auth_service.create_auth(credentials, db)

@app.post("/register")
async def register(data: UserBase, credentials: AuthBase, db: Session = Depends(get_db)):
    result = requests.post(url="/create_user", data=data.json())
    if not user_service.is_user_in_db_by_email(credentials.email, db) and result.status_code==201:
        credentials.uid = int(result.text)
        requests.post(url="/create_auth", data=credentials.json())
        return {"message": "User created"}
    else:
        raise HTTPException(status_code=409, detail="User already exists")


@app.post("/login")
async def login(credentials: AuthBase, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(credentials.email, credentials.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(
        data={"email": user[1].email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    )
    return {"token": access_token, "token_type": "bearer"}
