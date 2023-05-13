from fastapi import FastAPI, HTTPException
from pyparsing import Optional
from .controller import recommend_recipes
from schema import Message
app = FastAPI()

@app.post("/ia/predict")
async def predict(text:Message):
    return recommend_recipes(text.message)
    


@app.get("/ia/test")
async def test():
    return "ça marche"