from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase

from schemas.userSchema import UserSchema


class Base(DeclarativeBase):
    pass

class ChatSchema(Base):
    __tablename__ = 'chatmessage'
    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fromu = Column(String(100))
    text = Column(String(10000))
    user_uid = Column(Integer, ForeignKey(UserSchema.uid, ondelete="CASCADE"), nullable=False)

    def __init__(self, fromu: str, text: str, id_user: int):
        self.fromu = fromu
        self.text = text
        self.user_uid = id_user

    def __repr__(self):
        return f"<Chat(uid={self.uid}, fromu={self.fromu}, text={self.text}, id_user={self.id_user})>"