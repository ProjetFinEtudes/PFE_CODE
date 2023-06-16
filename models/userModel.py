from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    genre: str
    id_auth: int

    class Config:
        orm_mode = True

class User(BaseModel):
    uid: int
    first_name: str
    last_name: str
    birth_date: str
    genre: str