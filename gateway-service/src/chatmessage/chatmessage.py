from fastapi import APIRouter,Depends
from dotenv import load_dotenv
import os
import requests
from sqlalchemy import create_engine,select
from models.chatMessageModel import Conversation
from ..auth.token import get_current_user
from models import TokenData,Token
from models import chatModel 
from typing import Annotated
from sqlalchemy.orm import Session, sessionmaker
from schemas.authSchema import AuthSchema
load_dotenv()

CHATMESSAGE_URL = os.getenv("CHATMESSAGE_URL")
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
    prefix="/chat",
    tags=['chatbot']
)

@router.post('/chat_message')
def create_user_conversation(token: Annotated[TokenData,Depends(get_current_user)], conversation: Conversation,db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    response = requests.post(f"{CHATMESSAGE_URL}/save_chat?user_id={user_id}", data=conversation.json())
    return response.json() 
@router.get('/get_chat')
def get_chat(token: Annotated[TokenData,Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    response = requests.get(f"{CHATMESSAGE_URL}/get_chat?user_id={user_id}")
    return response.json()

@router.delete('/delete_chat')
def delete_chat(chat_id:int,token: Annotated[TokenData,Depends(get_current_user)]):
    response = requests.delete(f"{CHATMESSAGE_URL}/delete_chat?chat_id={chat_id}':delete_chat")
    return response.json()
@router.put('/update_chat')
def update_chat(token: Annotated[TokenData,Depends(get_current_user)],id_conv,update_conv:Conversation,db: Session = Depends(get_db)):
    user = db.execute(select(AuthSchema).where(AuthSchema.email == token.uid)).scalar_one_or_none()
    user_id = user.id_auth
    response = requests.put(f"{CHATMESSAGE_URL}/update_chat/{user_id}/{id_conv}",data=update_conv.json())
    return response.json()
# @app.put("/update_chat/{user_id}/{id_conv}")
# def update_user_conversation(user_id: int, id_conv: int, update_conversation: Conversation, db: Session = Depends(get_db)):
#     return Chatmessage.update_user_conversation(user_id, id_conv, update_conversation, db)
