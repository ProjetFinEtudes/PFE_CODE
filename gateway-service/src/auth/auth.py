import os
from typing import Annotated
import requests

from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from models.authModel import AuthBase
from models.userModel import UserBase
from models import Token
load_dotenv()

AUTH_URL = os.getenv("AUTH_URL")
USER_URL = os.getenv("USER_URL")

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.post("/register")
async def register(credentials: AuthBase, data: UserBase):
    result = requests.post(url=AUTH_URL, data=credentials.json())
    if (result.status_code == 201):
        data.id_auth = int(result.text)
        date = datetime.strptime(data.birth_date, "%a %b %d %Y %H:%M:%S GMT%z")
        data.birth_date = date.strftime("%Y-%m-%d")
        print(data.birth_date)

        response = requests.post(url=USER_URL, data=data.json())
        if (response.status_code == 201):
            return {"message": "User created"}
        else:
            raise HTTPException(status_code=response.status_code, detail="Unable to store user details")
    else:
        raise HTTPException(status_code=result.status_code, detail="Unable to create user")

@router.post('/login')
def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    credentials = AuthBase(email=credentials.username,password=credentials.password)
    result = requests.post(f"{AUTH_URL}/login", data=credentials.json())

    if (result.status_code == 200):
        return Token(access_token=result.json()['token'],token_type=result.json()['token_type'])
    else:
        raise HTTPException(status_code=result.status_code, detail=result.json()['detail'])