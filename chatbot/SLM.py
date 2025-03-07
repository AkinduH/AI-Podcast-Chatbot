import os
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
)

def can_provide_response(user_message, formatted_history):
    try:
        chat_session = model.start_chat()
        response = chat_session.send_message(
            f"Please respond with 'yes' only if the user message is significantly related "
            f"to the previous messages in the conversation history; otherwise, respond with 'no'.\n"
            f"User message:\n{user_message}\n"
            f"Formatted history:\n{formatted_history}"
        )

        
        response_content = response.text.strip()
        return ("yes" in response_content.lower())
    except Exception as e:
        print(f"An error occurred: {e}")
        return False