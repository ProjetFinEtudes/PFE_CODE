import json
from fastapi import APIRouter,Depends
from typing import Annotated
from dotenv import load_dotenv
import os
import requests
from schemas import Message
load_dotenv()

AUTH_URL = os.getenv("AUTH_URL")

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.post('/login')
def user_login():
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{AUTH_URL}/login", headers=headers)
    return response.json()
