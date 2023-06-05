from pydantic import BaseModel

class AuthBase(BaseModel):
    # id_auth: int
    email: str
    password: str
    uid: int

    class Config:
        orm_mode = True

# class Auth(AuthBase):
#     id_auth: int
#     uid: int

#     class Config:
#         orm_mode = True