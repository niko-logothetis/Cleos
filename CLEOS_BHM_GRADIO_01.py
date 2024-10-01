import requests
import json
import gradio as gr

# Set the API URL for the Langflow app
API_URL = "https://api.langflow.astra.datastax.com/lf/f885cef4-688b-4d3f-9686-14269ff4c163/api/v1/run/d6d67517-7e5d-4258-bec2-e1adce10b711"

# Application token for authorization
APPLICATION_TOKEN = "AstraCS:DTNlrfHBNaZGhwAOxQUtjOuo:8e084bc11b7061bc717a600e0b14d098288c96a6529cee67cc7b6fd6478c98eb"

# Function to query the Langflow API
def query_langflow_api(message):
    # Create the payload as expected by the API
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make a POST request to the Langflow API
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            json_response = response.json()
            # Extract the message text from the nested structure
            message_text = json_response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
            return message_text
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Failed to connect to the API: {e}"

# Gradio chat interface

def chat_response(message, history):
    # Send only the latest message (not the history) to the Langflow API
    response = query_langflow_api(message)
    
    # Update the chat history with the new user message and bot response
    # history.append(response)  # Append as a list, not a tuple
    
    return response

# Create the Gradio chat interface
interface = gr.ChatInterface(
    fn=chat_response,
    chatbot=gr.Chatbot(height=600, placeholder="Willkommen zum Cleos der Burghauptmannschaft. Ich stehe Ihnen für Fragen zur Verfügung."),

    textbox=gr.Textbox(placeholder="Bitte geben Sie hier Ihre Fragen ein", container=False, scale=7),
    title="Cleos",
    description="<strong><center>Sie können hier Fragen rund um das Thema der Burghauptmannschaft und der Hofburg stellen.<br>Sollten Sie einmal nicht weiter kommen, dann bitten Sie mich um Hilfe.</strong></center>",
    theme=gr.themes.Default(primary_hue="red"),
    examples=["Was gibt es Neues in der Hofburg?", "Wie sind die Öffnungszeiten?", "Gibt es Aktivitäten für Kinder?"],
    cache_examples=False,
    retry_btn="Erneut senden",
    undo_btn="Letzte Eingabe löschen",
    clear_btn="Clear",

    ).launch()


