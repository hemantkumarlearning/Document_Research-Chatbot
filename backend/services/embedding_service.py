# from sentence_transformers import SentenceTransformer 

#Load model
# model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
model = ""

def embed_text(text):

    if model:
    #Encoding text into vector representation
        return model.encode(text)
    else:
        return