# AI Podcast Chatbot

This repository contains a system for creating and interacting with an AI chatbot that can answer questions about Lex Fridman podcast interviews. The system processes podcast transcripts, creates vector databases for efficient retrieval, and provides a chat interface for users to ask questions about the content.

<div align="center">
  <a href="https://youtu.be/hV0jOnzFcdI?si=VOCYdYhFcp6bbert">
    <img src="https://github.com/CodeBustersCrafter/iwb350-cognic-ai/blob/main/Tumblain.jpg" alt="AI Podcast Chatbot Demo" width="600">
  </a>
  <br>
  <a href="https://youtu.be/hV0jOnzFcdI?si=VOCYdYhFcp6bbert">
    <img src="https://img.icons8.com/color/48/000000/youtube-play.png" alt="Play Video">
  </a>
  <br>
  <i>Watch the AI Podcast Chatbot Demo Video</i>
</div>

## Project Overview

The system consists of several key components:

1. **Transcript Processing**: Scripts to extract and structure podcast transcripts from Lex Fridman's website
2. **Vector Database Creation**: Tools to convert transcripts into searchable vector databases
3. **Retrieval System**: A context retrieval mechanism that finds relevant information from transcripts
4. **Chat Interface**: A Streamlit-based UI for interacting with the chatbot
5. **Backend API**: FastAPI endpoint that processes user queries and generates responses

## Key Components

### Data Extraction

The `data_extraction.py` script scrapes transcript data from Lex Fridman's website and structures it into JSON files. Each transcript entry includes:
- Speaker information
- Section topics
- Timestamps
- YouTube links
- Speech content

### Vector Database Creation

The `Creating_Vector_DBs.py` script:
- Processes JSON transcript files
- Chunks the text into manageable segments
- Creates FAISS vector databases using Hugging Face embeddings
- Saves the vector stores for efficient retrieval

### Chat Backend

The backend system (`Chat_Endpoint.py`) uses:
- Google's Gemini model for response generation
- A context retrieval system to find relevant transcript segments
- Session management to maintain conversation history

### User Interface

The `chat_ui.py` provides a Streamlit-based interface that:
- Displays the conversation history
- Accepts user input
- Communicates with the backend API
- Presents AI responses in a user-friendly format

## Getting Started

To run this project locally, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-podcast-chatbot.git
   cd ai-podcast-chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   Create a `.env` file in the root directory and add the following:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Run the components:**
   ```bash
   # Start the FastAPI backend
   python chatbot/Chat_Endpoint.py
   
   # In a separate terminal, start the Streamlit UI
   streamlit run chat_ui.py
   ```

## Supported Podcasts

The system currently includes transcripts from the following Lex Fridman podcast episodes:
- Yann LeCun (Episode #416)
- Sam Altman (Episode #419)
- Elon Musk (Episode #400)
- Ben Shapiro vs Destiny Debate (Episode #410)

## Technical Details

- **Embedding Model**: Uses "sentence-transformers/all-MiniLM-L6-v2" for creating vector embeddings
- **LLM**: Utilizes Google's Gemini 1.5 Flash model for generating responses
- **Vector Store**: FAISS for efficient similarity search
- **API Framework**: FastAPI for the backend service
- **UI Framework**: Streamlit for the user interface

## System Architecture

1. User submits a question through the Streamlit UI
2. The question is sent to the FastAPI backend
3. The backend retrieves relevant context from the vector databases
4. The context and question are sent to the Gemini model
5. The model generates a response based on the context and conversation history
6. The response is returned to the user interface

This system provides an interactive way to explore and learn from the rich content of Lex Fridman's podcast interviews through natural language conversation.
