from sqlalchemy.schema import Column
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class UserSchema(Base):
    __tablename__ = 'User'
    uid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(Date)
    genre = Column(String(1))
