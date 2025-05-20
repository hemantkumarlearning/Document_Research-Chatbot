from sentence_transformers import SentenceTransformer 

# Load the sentence-transformer model
model = SentenceTransformer('all-MiniLM-L6-v2') # Lightweight model with good performance

def embed_text(text):
    return model.encode(text) 