from fastapi import FastAPI
# from app.database import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally :
        db.close()

@app.post("/login")
async def user_login():
    return {"message": "Hello World"}
    # user = authenticate_user(email, password, db)
    # if not user:
    #     raise HTTPException(status_code=401, detail="Invalid email or password")
    # access_token = create_access_token(
    #     data={"email": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)}
    # )
    # return {"token": access_token, "token_type": "bearer"}
