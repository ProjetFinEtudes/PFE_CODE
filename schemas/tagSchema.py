from pymysql import Date
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .userSchema import  UserSchema
Base = declarative_base()


class TagSchema(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
class UserSchema(Base):
    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(String, nullable=False)
    genre = Column(String(1), nullable=False)
    id_auth = Column(Integer, nullable=False)
    user_tags = relationship("UserTagSchema", back_populates="user")
class UserTagSchema(Base):
    __tablename__ = 'user_tags'
    id_user = Column(Integer, ForeignKey('user.uid'), primary_key=True)
    id_tag = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    user = relationship(UserSchema, back_populates="user_tags")
    tag = relationship(TagSchema)