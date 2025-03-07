import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import uuid
import retrieve_context
import SLM
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


app = FastAPI()
chat_instances = {}
memory_instances = {}

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
genai.configure(api_key=gemini_api_key)

generation_config = {
    "temperature": 0.2,  
    "top_p": 0.95,      
    "top_k": 20,        
    "max_output_tokens": 6372,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

with open("chatbot/SYSTEM_PROMPT.txt", "r") as file:
    SYSTEM_PROMPT = file.read().strip()

class ChatMessage(BaseModel):
    message: str
    session_id: str = None

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        if not chat_message.session_id or chat_message.session_id not in chat_instances:
            session_id = str(uuid.uuid4())
            memory = ConversationBufferMemory(return_messages=True)
            chat_instance = model.start_chat()
            chat_instance.send_message({"role": "user", "parts": [{"text": SYSTEM_PROMPT}]})
            chat_instances[session_id] = chat_instance
            memory_instances[session_id] = memory
            chat_message.session_id = session_id
        else:
            print(chat_message.session_id)
            chat_instance = chat_instances[chat_message.session_id]
            memory = memory_instances[chat_message.session_id]

        chat_history = memory.load_memory_variables({}).get("history", [])
        conversation_log = []
        last_three_chats = chat_history[-3:]  # Get the last 3 chats
        for message in last_three_chats:
            if isinstance(message, HumanMessage):
                conversation_log.append(f"Human: {message.content}")
            elif isinstance(message, AIMessage):
                conversation_log.append(f"AI: {message.content}")

        formatted_history = "\n".join(conversation_log)
        context = ""

        if SLM.can_provide_response(chat_message.message,formatted_history) == True:
            print("Using history only")
            augmented_prompt = f"User question: {chat_message.message}\n\nconversation history:\n{formatted_history}\n\nTranscript context:\n{context}"
        else:
            print("Retriving..")
            context = retrieve_context.retrieve_context(chat_message.message) 

        augmented_prompt = f"User question: {chat_message.message}\n\nconversation history:\n{formatted_history}\n\nTranscript context:\n{context}"
        
        response = chat_instance.send_message(augmented_prompt)
        memory.save_context({"input": augmented_prompt}, {"output": response.text})
        
        print(response.text)  
        return {
            "response": response.text,
            "session_id": chat_message.session_id
        }
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
