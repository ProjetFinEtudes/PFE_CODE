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

RECO_URL = os.getenv("RECO_URL")
MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
router = APIRouter(
    prefix="/predict",
    tags=['recommendation']
)

@router.post('/')
def get_recommendation(text: Message,token: Annotated[TokenData,Depends(get_current_user)],db: Session = Depends(get_db)):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    response = requests.post(f"{RECO_URL}/predict?user_id={user_id}", headers=headers, data=text.json())
    return response.json()

@router.post('/getdish')
def get_dish(text: Message,token: Annotated[TokenData,Depends(get_current_user)]):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}/getdish", headers=headers, data=text.json())
    return response.json()