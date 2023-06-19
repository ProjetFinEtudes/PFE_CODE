from fastapi import APIRouter,Depends
from dotenv import load_dotenv
import os
import requests
from schemas import Message
from models import TokenData,Token
from models import chatModel 
from typing import Annotated

from schemas.authSchema import AuthSchema
from ..auth.token import get_current_user
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')
TAG_URL = os.getenv("TAG_URL")

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()




router = APIRouter(
    prefix="/tag",
    tags=['tag']
)

@router.post('/')
def create_tag(token: Annotated[TokenData,Depends(get_current_user)],tag_name:str,db: Session = Depends(get_db)):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    response = requests.post(f"{TAG_URL}/user_tags/create?user_id={user_id}&tag_name={tag_name}", headers=headers)
    return response.json()

@router.get('/get_all')
def get_all(token: Annotated[TokenData,Depends(get_current_user)]):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}       
    response = requests.get(f"{TAG_URL}/all_tags", headers=headers)
    return response.json()

@router.get('/get_user_tags')
def get_user_tags(token: Annotated[TokenData,Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}       
    response = requests.get(f"{TAG_URL}/user_tags/{user_id}", headers=headers)
    return response.json()
@router.delete('/user_tags/{user_id}/{tag_name}')
def delete_user_tag(tag_name:str,token: Annotated[TokenData,Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}       
    response = requests.get(f"{TAG_URL}/user_tags/{user_id}", headers=headers)
    return response.json()
