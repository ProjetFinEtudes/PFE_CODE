from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from .recommendation import recommendation
from .chatbot import chatbot
from .auth import auth
from .chatmessage import chatmessage
from .user import user
from .tags import tag
app = FastAPI()
subapi = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

subapi.include_router(recommendation.router)
subapi.include_router(chatbot.router)
subapi.include_router(auth.router)
subapi.include_router(chatmessage.router)
subapi.include_router(user.router)
subapi.include_router(tag.router)
app.mount("/api", subapi)