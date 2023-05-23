from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase

from schemas.userSchema import UserSchema

class Base(DeclarativeBase):
    pass

class AuthSchema(Base):
    __tablename__ = 'Auth'
    id_auth = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    uid = Column(Integer, ForeignKey(UserSchema.uid), nullable=False)