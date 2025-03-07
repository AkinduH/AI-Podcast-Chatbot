import os
import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def count_tokens(text):
    """Estimate token count using word count (approx 1.3 words per token)."""
    return len(text.split()) // 1.3

def create_vector_db(filename):
    """Creates a vector database from structured JSON transcript."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir,  "Transcripts", filename)

    # Load transcript JSON
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            transcript_data = json.load(file)
        print(f"File {filename} loaded successfully")
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Prepare chunks
    chunks = []
    current_chunk = []
    current_token_count = 0
    current_section = None

    for entry in transcript_data:
        section = entry["section_topic"]
        video = entry["full_video"]
        speaker = entry["speaker"]
        speech = entry["speech"]
        youtube_link = entry["youtube_link"]
        timestamp = entry["timestamp"]

        # If section changes, start a new chunk
        if section != current_section and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_token_count = 0

        # Format conversation text
        dialogue = f"**{speaker}**: {speech} on section {current_section}(specific video part : {youtube_link} on {video})"
        token_count = count_tokens(dialogue)

        # If adding this dialogue exceeds chunk size, save current chunk
        if current_token_count + token_count > CHUNK_SIZE:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_token_count = 0

        # Add to chunk
        current_chunk.append(dialogue)
        current_token_count += token_count
        current_section = section

    # Save last chunk if not empty
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    # Create vector database
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def create_and_save_vector_dbs():
    """Creates and saves vector stores for multiple transcripts."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    vector_dbs_dir = os.path.join(script_dir, "Vector DBs")
    os.makedirs(vector_dbs_dir, exist_ok=True)

    transcript_files = ["sam_altman_transcript.json", "elon_musk_transcript.json", "ben_shapiro_destiny_debate_transcript.json","yann_lecun_transcript.json"]

    for transcript in transcript_files:
        name = transcript.replace(".json", "")  # Remove extension
        vector_store = create_vector_db(transcript)

        if vector_store:
            save_path = os.path.join(vector_dbs_dir, f"{name}_vector_store")
            vector_store.save_local(save_path)
            print(f"Vector store '{name}' saved in '{vector_dbs_dir}'")
        else:
            print(f"Failed to create vector store for '{name}'")

if __name__ == "__main__":
    create_and_save_vector_dbs()
