from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from models.tagModel import UserTagBaseModel
from schemas.tagSchema import UserTagSchema
import os
from sqlalchemy.orm import Session, sessionmaker
from .controller.tag import *

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

@app.post("/user_tags/create", status_code=201)
def create_user_tag_endpoint(user_id: int, tag_name: str, db: Session = Depends(get_db)):
    user_tag = create_user_tag(user_id, tag_name, db)
    return user_tag
@app.get('/all_tags')
def get_tags(db: Session = Depends(get_db)):
    return get_all_tags(db)
@app.get("/user_tags/{user_id}")
def get_user_tags_endpoint(user_id: int, db: Session = Depends(get_db)):
    user_tags = get_user_tags(user_id, db)
    return user_tags

@app.delete("/user_tags/{user_id}/{tag_name}")
def delete_user_tag_endpoint(user_id: int, tag_name: str, db: Session = Depends(get_db)):
    deleted_count = delete_user_tag(user_id, tag_name, db)
    return {"message": "User tag deleted successfully"}

