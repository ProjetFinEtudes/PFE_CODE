from fastapi import FastAPI, HTTPException
from pyparsing import Optional

from .controller import rec
app = FastAPI()

@app.post("/ia/predict")
async def predict(text):
    return rec(text)
    


@app.get("/ia/test")
async def test():
    return "ça marche"