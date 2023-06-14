import os
import requests

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine

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
async def save_chat(data: ChatBase, db: Session = Depends(get_db)):
    return Chatmessage.save_chat(data, db)

