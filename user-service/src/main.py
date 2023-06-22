import os

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine

from .controller import user as user_controller
from sqlalchemy.orm import Session, sessionmaker

from models.authModel import AuthBase
from models.userModel import UserBase, User

app = FastAPI()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.post("/", status_code=201)
async def create_user(data: UserBase, db: Session = Depends(get_db)):
    return user_controller.create_user(data, db)

@app.get("/")
def get_user(uid: int, db: Session = Depends(get_db)):
    return user_controller.get_user_by_uid(uid, db)

@app.patch("/")
def update_user(user: User, db: Session = Depends(get_db)):
    return user_controller.update_user(user, db)


@app.delete("/")
def delete_user(uid: int, db: Session = Depends(get_db)):
    return user_controller.delete_user_by_uid(uid, db)