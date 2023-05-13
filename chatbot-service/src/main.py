from fastapi import FastAPI, HTTPException
from pyparsing import Optional
from schema import Message
from .controller import chatbot_endpoint
app = FastAPI()

@app.post("/chat")
async def predict(text: Message):
    return chatbot_endpoint(text)
