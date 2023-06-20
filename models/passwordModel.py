from pydantic import BaseModel

class PasswordBase(BaseModel):
    password: str

    class Config:
        orm_mode = True