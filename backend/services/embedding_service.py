# import requests
# import os
# import json

# EMBED_URL = os.getenv("EMBEDDING_URL")

# def embed_text(texts):
#     headers = {"Content-Type": "application/json"}
#     payload = {"texts": texts}

#     res = requests.post(f"{EMBED_URL}", headers=headers,data=json.dumps(payload))
#     return res.json()["embeddings"]

from sentence_transformers import SentenceTransformer 

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

def embed_text(text):
    return model.encode(text)
