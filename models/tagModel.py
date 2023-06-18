from pydantic import BaseModel

class UserTagBaseModel(BaseModel):
    id_user: int
    id_tag: int

class UserTagCreateModel(UserTagBaseModel):
    pass

class UserTagModel(UserTagBaseModel):
    class Config:
        orm_mode = True
