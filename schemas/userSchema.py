from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy import Integer, String, Date, CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

from schemas.authSchema import AuthSchema


class Base(DeclarativeBase):
    pass

class UserSchema(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(Date)
    genre = Column(CHAR)
    id_auth = Column(Integer, ForeignKey(AuthSchema.id_auth, ondelete="CASCADE"), nullable=False)

    def __init__(self, first_name: str, last_name: str, birth_date: Date, genre: str, id_auth: int):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.genre = genre
        self.id_auth = id_auth

    def __repr__(self):
        return f"<User(uid={self.uid}, first_name={self.first_name}, last_name={self.last_name}, birth_date={self.birth_date}, genre={self.genre}, id_auth={self.id_auth})>"