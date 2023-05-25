import os

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from .controller.authentication import authenticate_user
from .controller.security import create_access_token
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally :
        db.close()

@app.post("/login")
async def user_login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(email, password, db)
    print(user)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(
        data={"email": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    )
    return {"token": access_token, "token_type": "bearer"}
