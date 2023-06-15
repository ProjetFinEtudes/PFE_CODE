import os
import json
import requests

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from datetime import datetime

from models.authModel import AuthBase
from models.userModel import UserBase

load_dotenv()

AUTH_URL = os.getenv("AUTH_URL")

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.post("/register")
async def register(credentials: AuthBase, data: UserBase):
    result = requests.post(url=f"{AUTH_URL}/create_auth", data=credentials.json())
    if (result.status_code == 201):
        data.id_auth = int(result.text)
        date = datetime.strptime(data.birth_date, "%a %b %d %Y %H:%M:%S GMT%z")
        data.birth_date = date.strftime("%Y-%m-%d")

        response = requests.post(url=f"{AUTH_URL}/create_user", data=data.json())
        if (response.status_code == 201):
            return {"message": "User created"}
        else:
            raise HTTPException(status_code=response.status_code, detail="Unable to store user details")
    else:
        raise HTTPException(status_code=result.status_code, detail="Unable to create user")

@router.post('/login')
def user_login(credentials: AuthBase):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    text = {'email': credentials.email, 'password': credentials.password}
    response = requests.post(f"{AUTH_URL}/login", headers=headers, data=json.dumps(text))
    return response.json()