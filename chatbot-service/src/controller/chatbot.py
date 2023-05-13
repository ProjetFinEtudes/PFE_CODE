import json
from .neuralintent.main import GenericAssistant
from schema import Message
from dotenv import load_dotenv
import requests
import os
new_assistant = GenericAssistant('/code/src/controller/intents.json')
new_assistant.load_model(model_name='food_recommendation_model')
done = False
# Start the assistant
load_dotenv()

RECO_URL = os.getenv("RECO_URL")

def food_ingredients_reco(message:Message):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}", headers=headers, data=message.json())
    recipe_list = response.json()
    recipe_names = [recipe['name'] for recipe in recipe_list]
    result = "Here's a recipe list:\n" + "\n".join(recipe_names)
    return result
def chatbot_endpoint(message: Message):
    ints=new_assistant._predict_class(message.message)
    if ints[0]['intent'] == 'food_recommendation_by_ingredients':
        response=food_ingredients_reco(message)
        return {"response":response}
    bot_response = new_assistant.request(message.message)
    return {"response": bot_response}