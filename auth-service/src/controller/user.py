from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import exists

from schemas.authSchema import AuthSchema
from schemas.userSchema import UserSchema

from models.userModel import UserBase, User

class User:

    def get_user_info_by_email(self, email: str, db: Session):
        auth_item = db.query(AuthSchema).filter_by(email=email).first()
        if auth_item:
            user_item = db.query(UserSchema).filter_by(uid=auth_item.uid).first()
            if user_item:
                user_info = db.query(UserSchema, AuthSchema) \
                    .join(AuthSchema, UserSchema.uid == AuthSchema.uid) \
                    .filter(AuthSchema.email == email) \
                    .first()
                return user_info
        return None
    
    def get_user_by_uid(self, uid: int, db: Session):
        user_item = db.query(UserSchema).filter_by(uid=uid).first()
        if user_item:
            pydantic_user = UserBase.from_orm(user_item)
            return pydantic_user
        return None
    
    def get_all_users(self, db: Session):
        try:
            user_items = db.query(UserSchema).all()
            if user_items:
                pydantic_users = [UserBase.from_orm(user_item) for user_item in user_items]
                return pydantic_users
            else:
                raise HTTPException(status_code=404, detail="No users found")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e.__dict__['orig']))
        
    def is_user_in_db_by_email(self, email: str, db: Session):
        return db.query(exists().where(UserSchema.email == email)).scalar()
    
    def is_user_in_db_by_uid(self, uid: int, db: Session):
        return db.query(exists().where(UserSchema.uid == uid)).scalar()
    
    def get_user_id(self, email: str, db: Session):
        try:
            if self.is_user_in_db_by_email(email, db):
                pydantic_user = self.get_user_by_email(email, db)
                return pydantic_user.uid
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e.__dict__['orig']))
        
    def create_user(self, user: UserBase, db: Session):
        try:
            if not self.is_user_in_db_by_uid(user.uid, db):
                pydantic_user = UserSchema(**user.dict())
                db.add(pydantic_user)
                db.commit()
                db.refresh(pydantic_user)
                return {'message': 'User created successfully'}
            else:
                raise HTTPException(status_code=409, detail="User already exists")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e.__dict__['orig']))
        
    def delete_user(self, user: UserBase, db: Session):
        try:
            if self.is_user_in_db_by_uid(user.uid, db):
                db.query(UserSchema).filter_by(uid=user.uid).delete()
                db.commit()
                return {'message': 'User deleted successfully'}
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e.__dict__['orig']))

    def update_user(self, user: UserBase, db: Session):
        try:
            if self.is_user_in_db_by_uid(user.uid, db):
                db.query(UserSchema).filter_by(uid=user.uid).update(user.dict())
                db.commit()
                return {'message': 'User updated successfully'}
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e.__dict__['orig']))
