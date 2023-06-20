import os
import requests

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine

from models.chatMessageModel import Conversation

from .controller.chatmessage import Chatmessage
from sqlalchemy.orm import Session, sessionmaker

from models.chatModel import ChatBase
from models.userModel import UserBase

app = FastAPI()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
chatmessage_service = Chatmessage()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.post("/save_chat")
def create_user_conversation(user_id: int, conversation: Conversation, db: Session = Depends(get_db)):
    return Chatmessage.create_user_conversation(user_id,conversation,db)
@app.get("/get_chat")
def get_user_conversation(user_id:int,db: Session = Depends(get_db)):
    return Chatmessage.get_user_conversations(user_id,db)
@app.delete("/delete_chat")
def delete_user_conv(chat_id,db: Session = Depends(get_db)):
    return Chatmessage.delete_chat(chat_id,db)
@app.put("/update_chat/{user_id}/{id_conv}")
def update_user_conversation(user_id: int, id_conv: int, update_conversation: Conversation, db: Session = Depends(get_db)):
    return Chatmessage.update_user_conversation(user_id, id_conv, update_conversation, db)
