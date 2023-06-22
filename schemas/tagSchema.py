from sqlalchemy import Date, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from schemas.authSchema import AuthSchema
from schemas.userSchema import UserSchema
Base = declarative_base()


class TagSchema(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    
class UserSchema(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    genre = Column(String(1), nullable=False)
    id_auth = Column(Integer, ForeignKey(AuthSchema.id_auth, ondelete="CASCADE"), nullable=False)
    user_tags = relationship("UserTagSchema", back_populates="user")

    def __init__(self, first_name: str, last_name: str, birth_date: Date, genre: str, id_auth: int):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.genre = genre
        self.id_auth = id_auth

    def __repr__(self):
        return f"<User(uid={self.uid}, first_name={self.first_name}, last_name={self.last_name}, birth_date={self.birth_date}, genre={self.genre}, id_auth={self.id_auth})>"

class UserTagSchema(Base):
    __tablename__ = 'user_tags'
    id_user = Column(Integer, ForeignKey(UserSchema.uid, ondelete="CASCADE"), primary_key=True)
    id_tag = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    user = relationship(UserSchema, back_populates="user_tags")
    tag = relationship(TagSchema)