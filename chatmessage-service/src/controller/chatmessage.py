from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordBearer

from models.chatModel import ChatBase

from schemas.chatSchema import ChatSchema

class Chatmessage:

    def save_chat(self, chat: ChatBase, db: Session):
 
        pydantic_chat = ChatSchema(fromu=chat.fromu,
                                   text=chat.text,
                                   id_user=chat.user_uid)
        print(pydantic_chat)
        try:
            db.add(pydantic_chat)
            db.commit()
            db.refresh(pydantic_chat)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Could not create chat")
        return pydantic_chat.uid