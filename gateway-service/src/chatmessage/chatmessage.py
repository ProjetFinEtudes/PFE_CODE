from fastapi import APIRouter,Depends
from dotenv import load_dotenv
import os
import requests
from schemas import Message
load_dotenv()

CHATMESSAGE_URL = os.getenv("CHATMESSAGE_URL")

router = APIRouter(
    prefix="/chat",
    tags=['chatbot']
)

@router.post('/chat_message')
def get_chatResp(text: Message):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{CHAT_URL}/chat", headers=headers, data=text.json())
    return response.json()
