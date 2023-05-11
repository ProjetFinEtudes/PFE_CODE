from gradio_client import Client

client = Client("https://carperai-stablevicuna.hf.space/")
result = client.predict(
				"Salut!",	# str representing string value in 'Send a message' Textbox component
				"null",	# str representing filepath to JSON file in 'parameter_4' Chatbot component
				fn_index=0
)
print(result)