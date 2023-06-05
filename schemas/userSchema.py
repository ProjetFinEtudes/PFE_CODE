from sqlalchemy.schema import Column
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class UserSchema(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(Date)
    genre = Column(String(1))

    def __init__(self, first_name: str, last_name: str, birth_date: Date, genre: str):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.genre = genre

    def __repr__(self):
        return f"<User(uid={self.uid}, first_name={self.first_name}, last_name={self.last_name}, birth_date={self.birth_date}, genre={self.genre})>"