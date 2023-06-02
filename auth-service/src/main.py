import os

from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine

from .controller.authentication import Authentication
from .controller.user import User
from .controller.security import create_access_token
from sqlalchemy.orm import Session, sessionmaker

from models.authModel import AuthBase, Auth
from models.userModel import UserBase

app = FastAPI()

MYSQL_DATABASE_URL= os.getenv('MYSQL_DATABASE_URL')

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
auth = Authentication()
user = User()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# créer model userauth

@app.post("/register")
async def register(data: UserBase, credentials: Auth, db: Session = Depends(get_db)):
    if not user.is_user_in_db_by_email(credentials.email, db):
        pydantic_user = user.create_user(data, db)
        print(pydantic_user)
        pydantic_auth = auth.create_auth(credentials, db)
        print(pydantic_auth)

        return {"message": "User created"}
    else:
        raise HTTPException(status_code=409, detail="User already exists")
    # a = auth.create_auth(credentials, db)
    # if not u or not a:
    #     raise HTTPException(status_code=401, detail="Invalid email or password")
    # access_token = create_access_token(
    #     data={"email": user[1].email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    # )
    # return {"token": access_token, "token_type": "bearer"}

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
async def login(credentials: AuthBase, db: Session = Depends(get_db)):
    user = auth.authenticate_user(credentials.email, credentials.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(
        data={"email": user[1].email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    )
    return {"token": access_token, "token_type": "bearer"}
