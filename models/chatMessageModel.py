from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    fromu: str
    text: str

class Conversation(BaseModel):
    messages: List[ChatMessage]