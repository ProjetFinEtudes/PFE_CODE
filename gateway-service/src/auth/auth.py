import os
import json
import requests

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

from models.authModel import AuthBase
from models.userModel import UserBase

load_dotenv()

AUTH_URL = os.getenv("AUTH_URL")

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.post('/login')
def user_login(credentials: AuthBase):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    text = {'email': credentials.email, 'password': credentials.password}
    response = requests.post(f"{AUTH_URL}/login", headers=headers, data=json.dumps(text))
    return response.json()

@router.post("/register")
async def register(data: UserBase, credentials: AuthBase):
    result = requests.post(url=f"{AUTH_URL}/create_auth", data=credentials.json())
    if result.status_code==201:
        data.id_auth = int(result.text)
        requests.post(url=f"{AUTH_URL}/create_user", data=data.json())
        return {"message": "User created"}
    else:
        raise HTTPException(status_code=409, detail="User already exists")