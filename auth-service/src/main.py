import os

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from .controller.authentication import Authentication
from .controller.security import create_access_token
from sqlalchemy.orm import Session, sessionmaker
from models.authModel import AuthBase

app = FastAPI()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
auth = Authentication()

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally :
        db.close()

# @app.post("/register")
# async def user_register(credentials: AuthBase, db: Session = Depends(get_db)):
#     user = auth.authenticate_user(credentials.email, credentials.password, db)

#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
#     access_token = create_access_token(
#         data={"email": user[1].email, "exp": datetime.utcnow() + timedelta(minutes=30)}
#     )
#     return {"token": access_token, "token_type": "bearer"}

@app.post("/login")
async def user_login(credentials: AuthBase, db: Session = Depends(get_db)):
    user = auth.authenticate_user(credentials.email, credentials.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(
        data={"email": user[1].email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    )
    return {"token": access_token, "token_type": "bearer"}
