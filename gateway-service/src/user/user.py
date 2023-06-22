import os
import requests

from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models.userModel import User
from models.models import TokenData
from schemas.authSchema import AuthSchema
from schemas.userSchema import UserSchema
from ..auth.token import get_current_user
from dotenv import load_dotenv


load_dotenv()
MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

USER_URL = os.getenv("USER_URL")

router = APIRouter(
    prefix="/user",
    tags=['user']
)

@router.get('/')
def get_user(token: Annotated[TokenData, Depends(get_current_user)], db: Session = Depends(get_db)):
    user_item = db.execute(
        select(UserSchema)
        .join(AuthSchema, AuthSchema.id_auth == UserSchema.id_auth)
        .where(AuthSchema.email == token.uid)
        ).scalar_one_or_none()
    
    response = requests.get(f"{USER_URL}/?uid={user_item.uid}")
    return response.json()

@router.patch('/')
def update_user(user:User, token: Annotated[TokenData,Depends(get_current_user)], db: Session = Depends(get_db)):
    user_item = db.execute(
        select(UserSchema)
        .join(AuthSchema, AuthSchema.id_auth == UserSchema.id_auth)
        .where(AuthSchema.email == token.uid)
        ).scalar_one_or_none()

    user.uid = user_item.uid
    response=requests.patch(url=USER_URL, data=user.json())
    return response.json()

