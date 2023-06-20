from typing import Annotated
from fastapi import APIRouter,Depends
from dotenv import load_dotenv
import os
import requests
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session, sessionmaker

from schemas import Message
from schemas.authSchema import AuthSchema
from ..auth.token import get_current_user
from models import TokenData,Token
load_dotenv()

CHAT_URL = os.getenv("CHAT_URL")

router = APIRouter(
    prefix="/chat",
    tags=['chatbot']
)
MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
@router.post('/chat')
def get_chatResp(text: Message,token: Annotated[TokenData,Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{CHAT_URL}/chat?user_id={user_id}", headers=headers, data=text.json())
    return response.json()
@router.get('/test')
def get_users_by_group(token: Annotated[TokenData,Depends(get_current_user)]):
        return token