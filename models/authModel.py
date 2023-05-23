from pydantic import BaseModel

class Auth(BaseModel):
    id_auth: int
    email: str
    password: str
    uid: int
    class Config:
        orm_mode = True