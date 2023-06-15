from fastapi import FastAPI, HTTPException
from pyparsing import Optional
from .controller import recommend_recipes
from .controller import dish_step
from schemas import Message
app = FastAPI()

@app.post("/ia/predict")
async def predict(text:Message):
    return recommend_recipes(text.message)
    

@app.post("/ia/getdish")
async def getdish(text:Message):
    return dish_step(text.message)

@app.get("/ia/test")
async def test():
    return "ça marche"