from pydantic import BaseModel
from datetime import date

class ChatBase(BaseModel):
    fromu: str
    text: str
    user_uid: int

    class Config:
        orm_mode = True