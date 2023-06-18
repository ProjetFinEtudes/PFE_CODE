from fastapi import APIRouter,Depends
from dotenv import load_dotenv
import os
import requests
from schemas import Message
from models import TokenData,Token
from models import chatModel 
from typing import Annotated
from ..auth.token import get_current_user
load_dotenv()

RECO_URL = os.getenv("RECO_URL")

router = APIRouter(
    prefix="/predict",
    tags=['recommendation']
)

@router.post('/')
def get_recommendation(text: Message,token: Annotated[TokenData,Depends(get_current_user)]):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}/predict", headers=headers, data=text.json())
    return response.json()

@router.post('/getdish')
def get_dish(text: Message,token: Annotated[TokenData,Depends(get_current_user)]):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}/getdish", headers=headers, data=text.json())
    return response.json()