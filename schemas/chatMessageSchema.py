from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
class UserConversation(Base):
    __tablename__ = "user_conv"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    conversation = Column(JSON)
