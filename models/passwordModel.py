from pydantic import BaseModel

class PasswordBase(BaseModel):
    current_password: str
    new_password: str

    class Config:
        orm_mode = True