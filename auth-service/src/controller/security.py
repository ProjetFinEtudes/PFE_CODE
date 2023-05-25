from datetime import datetime,timedelta
from typing import Optional
from jose import jwt
from dotenv import load_dotenv
import os
load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt