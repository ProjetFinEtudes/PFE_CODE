from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordBearer

from .user import User
from models.authModel import AuthBase

from schemas.authSchema import AuthSchema

class Authentication:

    def __init__(self):
        self.userService = User()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

    def create_auth(self, auth: AuthBase, db: Session):
        pydantic_auth = AuthSchema(email=auth.email,
                                   password=auth.password)
        print(pydantic_auth)
        try:
            db.add(pydantic_auth)
            db.commit()
            db.refresh(pydantic_auth)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email already registered")
        return pydantic_auth.id_auth

    def verify_password(self, plain_password, hashed_password):
        return plain_password == hashed_password

    def authenticate(self, email: str, password: str, db: Session):
        user_info = self.userService.get_user_info_by_email(email, db)

        if user_info:
            (user, auth) = user_info
        else:
            raise HTTPException(status_code=404, detail="User not found")

        if not self.verify_password(password, auth.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user_info
    
    
    # def get_user_from_token(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not resolve credentials"
    #     )
    #     try:
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    #         email: str = payload.get('email')
    #         exp: int = int(payload.get('exp'))
    #         if datetime.utcnow() > datetime.fromtimestamp(exp):
    #             raise credentials_exception
    #         if email is None:
    #             raise credentials_exception
    #     except JWTError:
    #         raise credentials_exception
    #     user = service.get_user_withid_by_email(email, db)
    #     if user is None:
    #         raise credentials_exception
    #     return user