from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError

from schemas.authSchema import AuthSchema
from schemas.userSchema import UserSchema

from models.userModel import UserBase
from models.authModel import AuthBase


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
        pydantic_user = UserSchema(first_name=user.first_name, \
                                   last_name=user.last_name, \
                                   birth_date=user.birth_date, \
                                   genre=user.genre, \
                                   id_auth=user.id_auth)
        print(pydantic_user)
        try:        
            db.add(pydantic_user)
            db.commit()
            db.refresh(pydantic_user)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Could not create user")
        return pydantic_user.uid
        
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
