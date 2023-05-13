import json
from neuralintents import GenericAssistant
import asyncio


new_assistant = GenericAssistant('./intents.json')
new_assistant.load_model(model_name='food_recommendation_model')
done = False
# Start the assistant
def chatbot_endpoint(message):
    bot_response = new_assistant.request(message)
    return {"response": bot_response}

print(chatbot_endpoint('hello'))
