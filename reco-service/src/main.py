from fastapi import FastAPI, HTTPException
from pyparsing import Optional

from .controller import recommend_recipes
app = FastAPI()

@app.post("/ia/predict")
async def predict(text):
    return recommend_recipes(text)
    


@app.get("/ia/test")
async def test():
    return "ça marche"