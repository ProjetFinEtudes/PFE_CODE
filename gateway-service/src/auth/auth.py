import json
from fastapi import APIRouter,Depends
from dotenv import load_dotenv
import os
import requests
from models.authModel import AuthBase

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
