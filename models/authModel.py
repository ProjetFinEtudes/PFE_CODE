from pydantic import BaseModel

class AuthBase(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class Auth(AuthBase):
    id_auth: int