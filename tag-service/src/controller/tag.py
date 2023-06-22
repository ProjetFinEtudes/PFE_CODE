from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import os
from models.tagModel import UserTagBaseModel
from schemas.tagSchema import UserTagSchema, TagSchema

def create_user_tag(user_id:int, tag_name:str, db: Session):
    user_tag = UserTagBaseModel(id_user=user_id,id_tag=get_tag_id_by_name(tag_name,db))
    print(user_tag)
    pydantic_user_tag = UserTagSchema(**user_tag.dict())
    print(pydantic_user_tag)
    try:
        db.add(pydantic_user_tag)
        db.commit()
        db.refresh(pydantic_user_tag)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Unable to create user_tag entity")
    return pydantic_user_tag
def get_user_tags(user_id: int, db: Session):
    try:
        user_tags = db.query(UserTagSchema).filter(UserTagSchema.id_user == user_id).all()
        tags_name = []
        for user_tag in user_tags:
            tag_name = get_tag_name_by_id(user_tag.id_tag,db)
            tags_name.append(tag_name)
        return tags_name
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to fetch user tags")
def get_all_tags(db:Session):
    try:
        tags = db.query(TagSchema).all()
        return tags
    except SQLAlchemyError:
        raise HTTPException(status_code=50,detail="Unable to fetchs tag")    

def delete_user_tag(user_id: int, tag_name: str, db: Session):
    tag_id = get_tag_id_by_name(tag_name,db)
    deleted_count = db.query(UserTagSchema).filter_by(id_user=user_id, id_tag=tag_id).delete()
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="User tag not found")
    db.commit()
    return {"message": "User tag deleted successfully"}

def get_tag_id_by_name(name: str, db: Session):
    try:
        tag = db.query(TagSchema).filter(TagSchema.name==name).first()
        if tag:
            return tag.id
        else:
            raise HTTPException(status_code=404, detail="Tag not found")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to fetch tag")
def get_tag_name_by_id(id: int, db: Session):
    try:
        tag = db.query(TagSchema).filter(TagSchema.id==id).first()
        if tag:
            return tag.name
        else:
            raise HTTPException(status_code=404, detail="Tag not found")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to fetch tag")