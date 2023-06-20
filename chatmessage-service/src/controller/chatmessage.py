from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordBearer
from fastapi import  Depends
from sqlalchemy.orm import Session
from models.chatModel import ChatBase
from models.chatMessageModel import Conversation
from schemas.chatSchema import ChatSchema
from schemas.chatMessageSchema import UserConversation
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
    def create_user_conversation(user_id: int, conversation: Conversation, db: Session ):
        db_conversation = UserConversation(user_id=user_id, conversation=conversation.json())
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        return db_conversation 
    def get_user_conversations(user_id: int,db: Session ):
        conversations = db.query(UserConversation).filter(UserConversation.user_id == user_id).all()
        return conversations
    def delete_chat(chat_id: int, db: Session):
        chat = db.query(UserConversation).filter(UserConversation.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        try:
            db.delete(chat)
            db.commit()
            return {"deleted"}
        except SQLAlchemyError as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=400, detail="Could not delete chat")