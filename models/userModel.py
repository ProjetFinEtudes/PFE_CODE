from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    uid: int
    first_name: str
    last_name: str
    birth_date: date
    genre: str

    class Config:
        orm_mode = True

class User(UserBase):
    uid: int

    class Config:
        orm_mode = True