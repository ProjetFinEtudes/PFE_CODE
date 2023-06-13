from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class AuthSchema(Base):
    __tablename__ = 'auth'
    id_auth = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<Auth(id_auth={self.id_auth}, email={self.email}, password={self.password})>"