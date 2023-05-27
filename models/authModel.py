from pydantic import BaseModel

class AuthBase(BaseModel):
    email: str
    password: str

class Auth(AuthBase):
    id_auth: int
    uid: int

    class Config:
        orm_mode = True