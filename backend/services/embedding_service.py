# from sentence_transformers import SentenceTransformer 

# # Load the sentence-transformer model
# model = SentenceTransformer('all-MiniLM-L6-v2') # Lightweight model with good performance
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_text(text: str, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

  # Replace with your actual key

