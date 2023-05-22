from sqlalchemy.schema import Column
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class AuthSchema(Base):
    __tablename__ = 'Auth'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(Text, nullable=False)