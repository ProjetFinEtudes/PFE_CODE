from typing import Annotated
from fastapi import APIRouter,Depends
from dotenv import load_dotenv
import os
import requests
from schemas import Message
from ..auth.token import get_current_user
from models import TokenData,Token
load_dotenv()

CHAT_URL = os.getenv("CHAT_URL")

router = APIRouter(
    prefix="/chat",
    tags=['chatbot']
)

@router.post('/chat')
def get_chatResp(text: Message,token: Annotated[TokenData,Depends(get_current_user)]):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{CHAT_URL}/chat", headers=headers, data=text.json())
    return response.json()
@router.get('/test')
def get_users_by_group(token: Annotated[TokenData,Depends(get_current_user)]):
        return token