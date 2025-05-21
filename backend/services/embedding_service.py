from sentence_transformers import SentenceTransformer 

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

def embed_text(text):
    return model.encode(text)
