
import os
from typing import Annotated

from sqlalchemy import create_engine,select

from models.userModel import User
from ..auth.token import get_current_user
import requests
from schemas.authSchema import AuthSchema

from fastapi import APIRouter, Depends
from dotenv import load_dotenv
from models.models import TokenData
from sqlalchemy.orm import Session, sessionmaker

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
def get_user(token: Annotated[TokenData,Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    response =  requests.get(f"{USER_URL}/?uid={user_id}")
    return response.json()
@router.patch('/')
def update_user(user:User,token: Annotated[TokenData,Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    user.uid = user_id
    response=requests.patch(f"{USER_URL}/",data=user.json())
    return response.json()

