from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError

from schemas.tagSchema import UserSchema

from models.userModel import UserBase, User

def create_user(user: UserBase, db: Session):
    pydantic_user = UserSchema(first_name=user.first_name, \
                                last_name=user.last_name, \
                                birth_date=user.birth_date, \
                                genre=user.genre, \
                                id_auth=user.id_auth)
    try:        
        db.add(pydantic_user)
        db.commit()
        db.refresh(pydantic_user)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Unable to create user entity")
    return pydantic_user.uid


def get_user_by_uid(uid: int, db: Session):
    user_item = db.query(UserSchema).filter_by(uid=uid).first()
    if user_item:
        return user_item
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
def update_user(user: User, db: Session):
    user_item = db.query(UserSchema).filter_by(uid=user.uid).first()
    if user_item is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_item, key, value)
    db.add(user_item)
    db.commit()
    db.refresh(user_item)
    return user_item

def delete_user_by_uid(uid: int, db: Session):
    try:
        db.query(UserSchema).filter_by(uid=uid).delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete user")
    return {"message": "User deleted successfully"}
