from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordBearer

from models.authModel import AuthBase, Auth

from schemas.authSchema import AuthSchema
from schemas.userSchema import UserSchema

def create_auth(credentials: AuthBase, db: Session):
    pydantic_auth = AuthSchema(email=credentials.email,
                                password=credentials.password)
    print(pydantic_auth)
    try:
        db.add(pydantic_auth)
        db.commit()
        db.refresh(pydantic_auth)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return pydantic_auth.id_auth

def get_auth_by_id(id_auth: int, db: Session):
    auth_item = db.query(AuthSchema).filter_by(id_auth=id_auth).first()
    if auth_item:
        return auth_item
    else:
        raise HTTPException(status_code=404, detail="Auth not found")
    
def get_auth_by_email(email: str, db: Session):
    auth_item = db.query(AuthSchema).filter_by(email=email).first()
    if auth_item:
        return auth_item
    else:
        raise HTTPException(status_code=404, detail="Auth not found")
    
def update_auth(auth: Auth, db: Session):
    auth_item = db.query(AuthSchema).filter_by(id_auth=auth.id_auth).first()
    if auth_item is None:
        raise HTTPException(status_code=404, detail="Auth not found")
    
    auth_data = auth.dict(exclude_unset=True)
    for key, value in auth_data.items():
        setattr(auth_item, key, value)
    db.add(auth_item)
    db.commit()
    db.refresh(auth_item)
    return auth_item


def delete_auth_by_id(id_auth: int, db: Session):
    try:
        db.query(AuthSchema).filter_by(id_auth=id_auth).delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete user")
    return {"message": "User deleted successfully"}
    
def get_user_info_by_email(email: str, db: Session):
    auth_item = db.query(AuthSchema).filter_by(email=email).first()
    if auth_item:
        user_item = db.query(UserSchema).filter_by(id_auth=auth_item.id_auth).first()
        if user_item:
            user_info = db.query(UserSchema, AuthSchema) \
                .join(AuthSchema, UserSchema.id_auth == AuthSchema.id_auth) \
                .filter(AuthSchema.email == email) \
                .first()
            return user_info
    return None

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def authenticate(credentials: AuthBase, db: Session):
    user_info = get_user_info_by_email(credentials.email, db)
    print(user_info)
    if user_info:
        (user, auth) = user_info
    else:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(credentials.password, auth.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return user_info