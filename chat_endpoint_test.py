# import requests
# import uuid

# def test_chat_endpoint():
#     url = "http://localhost:8000/chat"

    
#     session_id = None
    
#     while True:
#         # Get user input
#         user_message = input("\nEnter your message (or 'quit' to exit): ")
        
#         if user_message.lower() == 'quit':
#             break
            
#         # Prepare the request payload
#         payload = {"message": user_message}
        
#         try:
#             # Send POST request to the chat endpoint
#             response = requests.post(url, json=payload)
            
#             # Check if request was successful
#             if response.status_code == 200:
#                 result = response.json()
#                 print("\nAssistant:", result["response"])
                
#                 if session_id is None:
#                     session_id = result["session_id"]
                
#             else:
#                 print(f"\nError: Request failed with status code {response.status_code}")
#                 print("Error message:", response.text)
                
#         except requests.exceptions.RequestException as e:
#             print(f"\nError making request: {e}")

# # Test the endpoint
# if __name__ == "__main__":
#     test_chat_endpoint()
