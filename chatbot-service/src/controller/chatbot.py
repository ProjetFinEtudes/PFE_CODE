import json
from .neuralintent.main import AIAssistant
from schemas import Message
from dotenv import load_dotenv
import requests
import os
new_assistant = AIAssistant('/code/src/controller/intents.json')
new_assistant.load_model(model_name='food_recommendation_model')
done = False
# Start the assistant
load_dotenv()

RECO_URL = os.getenv("RECO_URL")
def dish_step_reco(message:Message):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}/getdish", headers=headers, data=message.json())
    dish_steps = response.json()
    print(response)
    result = new_assistant.handle_request(message.message) + "\n" + dish_steps
    print(result)
    return result   
def food_ingredients_reco(message:Message,user_id:int):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response = requests.post(f"{RECO_URL}/predict?user_id={user_id}", headers=headers, data=message.json())
    recipe_list = response.json()
    print(recipe_list)
    recipe_names = [recipe for recipe in recipe_list]
    result =  new_assistant.handle_request(message.message) + "\n"+"Here's a recipe list:\n" + "\n".join(recipe_names)
    return result
def chatbot_endpoint(message: Message,user_id:int):
    ints=new_assistant._predict_intent(message.message)
    print(ints)
    if ints[0]['intent'] == 'food_recommendation_by_ingredients':
        response=food_ingredients_reco(message,user_id)
        return {"response":response}
    elif  ints[0]['intent'] == 'food_recommendation_by_dish_name':
        return {"response": dish_step_reco(message)}
    else:
        bot_response = new_assistant.handle_request(message.message)
        return {"response": bot_response}