from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    genre: str
    id_auth: int

    class Config:
        orm_mode = True