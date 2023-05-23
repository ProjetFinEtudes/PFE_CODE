import json
from fastapi import APIRouter,Depends
from typing import Annotated
from dotenv import load_dotenv
import os
import requests
from schemas import Message
load_dotenv()

RECO_URL = os.getenv("RECO_URL")

router = APIRouter(
    prefix="/predict",
    tags=['recommendation']
)

@router.post('/')
def get_recommendation(text: Message):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}/predict", headers=headers, data=text.json())
    return response.json()
@router.post('/getdish')
def get_dish(text: Message):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}/getdish", headers=headers, data=text.json())
    return response.json()