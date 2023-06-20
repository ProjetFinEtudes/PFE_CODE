from pydantic import BaseModel

class Password(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    class Config:
        orm_mode = True