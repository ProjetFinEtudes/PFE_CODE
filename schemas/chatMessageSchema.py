from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import DeclarativeBase

from schemas.userSchema import UserSchema

class Base(DeclarativeBase):
    pass
class UserConversation(Base):
    __tablename__ = "user_conv"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(UserSchema.uid, ondelete="CASCADE"), nullable=False)
    conversation = Column(JSON)
