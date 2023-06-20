from fastapi import FastAPI, HTTPException
from pyparsing import Optional
from schemas import Message
from .controller import chatbot_endpoint
app = FastAPI()

@app.post("/chat")
async def predict(text: Message,user_id:int):
    return chatbot_endpoint(text,user_id)
