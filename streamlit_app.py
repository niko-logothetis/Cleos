import streamlit as st
import requests
import json

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

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Callback function to handle user input and API response
def send_message():
    user_message = st.session_state.user_input.strip()
    
    if user_message:
        # Add user message to chat history
        st.session_state.messages.append({"role": "Visitor", "content": user_message})
        
        # Query the Langflow API with the user's message
        bot_response = query_langflow_api(user_message)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "Cleos", "content": bot_response})
        
        # Clear the input field
        st.session_state.user_input = ""

# Streamlit UI for ChatGPT-like window
st.image("https://sally-hair-extensions.com/wp-content/uploads/2024/09/BHM.png", use_column_width=True)

st.markdown("<h1 style='text-align: center;'>Willkommen zum Cleos</h1>", unsafe_allow_html=True)
st.write("Sie können hier Fragen rund um das Thema der Burghauptmannschaft stellen. Sollten Sie einmal nicht weiter kommen, dann bitten Sie mich um Hilfe.")

# CSS styling for rounded rectangles with gray tones
message_style_visitor = """
    background-color: #616161;  /* Light gray for visitor messages */
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
    color: #333333;  /* Dark gray for text */
    text-align: left;
    max-width: 60%;
"""

message_style_cleos = """
    background-color: #969696;  /* Slightly darker gray for Maha's messages */
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 15px;
    color: #333333;  /* Dark gray for text */
    text-align: left;
    max-width: 60%;
"""

# Display the chat messages
for message in st.session_state.messages:
    if message["role"] == "Visitor":
        st.markdown(f"<div style='{message_style_visitor}'><b>Visitor:</b> {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='{message_style_cleos}'><b>Cleos:</b> {message['content']}</div>", unsafe_allow_html=True)

# Text input for the user's message with a callback function
st.text_input("Sie:", key="user_input", placeholder="Bitte geben Sie hier Ihre Frage ein...", on_change=send_message)

# Maintain the scroll position at the bottom
st.markdown("""
    <script>
    var text_area = document.querySelector('textarea');
    text_area.scrollIntoView({behavior: 'smooth'});
    </script>
    """, unsafe_allow_html=True)
