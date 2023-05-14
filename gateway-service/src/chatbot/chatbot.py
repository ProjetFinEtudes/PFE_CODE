import json
from fastapi import APIRouter,Depends
from typing import Annotated
from dotenv import load_dotenv
import os
import requests
from schema import Message
load_dotenv()

CHAT_URL = os.getenv("CHAT_URL")

router = APIRouter(
    prefix="/chat",
    tags=['chatbot']
)

@router.post('/chat')
def get_chatResp(text: Message):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{CHAT_URL}/chat", headers=headers, data=text.json())
    return response.json()
