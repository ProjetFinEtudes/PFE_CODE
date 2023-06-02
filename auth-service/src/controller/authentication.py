from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordBearer

from .user import User
from models.authModel import AuthBase, Auth

from schemas.authSchema import AuthSchema

class Authentication:

    def __init__(self):
        self.userService = User()
        self.oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

    def create_auth(self, auth: AuthBase, db: Session):
        try:
            pydantic_auth = AuthSchema(**auth.dict())
            db.add(pydantic_auth)
            db.commit()
            db.refresh(pydantic_auth)
            return pydantic_auth
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Could not create auth")

    def verify_password(self, plain_password, hashed_password):
        return plain_password == hashed_password

    def authenticate_user(self, email: str, password: str, db: Session):
        user = self.userService.get_user_info_by_email(email, db)
        print(user[1])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not self.verify_password(password, user[1].password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user
    
    def get_user_from_token(self, token: str, db: Session):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            email: str = payload.get('email')
            exp: int = int(payload.get('exp'))
            if datetime.utcnow() > datetime.fromtimestamp(exp):
                raise credentials_exception
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = self.userService.get_user_info_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user