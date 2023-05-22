from pydantic import BaseModel

class AuthBase(BaseModel):
    email: str

class AuthCreate(AuthBase):
    password: str

class Auth(AuthBase):
    uid: int
    class Config:
        orm_mode = True