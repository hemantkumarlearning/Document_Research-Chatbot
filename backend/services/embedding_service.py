from sentence_transformers import SentenceTransformer 

#Load model
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

def embed_text(text):

    #Encoding text into vector representation
    return model.encode(text)
