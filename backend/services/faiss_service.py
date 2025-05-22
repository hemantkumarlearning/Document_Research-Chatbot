import faiss
import numpy as np
import os
import pickle
from backend.services.embedding_service import embed_text

# Directory to save/load FAISS indices and metadata
SAVE_DIR = "backend/embedding_store"
# os.makedirs(SAVE_DIR,exist_ok=True)


def save_index_and_meta(doc_id, index, meta):

     # Save FAISS index
    faiss.write_index(index, os.path.join(SAVE_DIR, f"{doc_id}.index"))
    
     # Save associated metadata using pickle
    with open(os.path.join(SAVE_DIR, f"{doc_id}_meta.pkl"), "wb") as f:
        pickle.dump(meta, f)

# In-memory maps to hold FAISS indices and metadata per document
index_map={}
meta_map={}

#Embed paragraphs, create a FAISS index, and store both in memory and on disk.
def embed_and_store(doc_id,paragraphs):

     # Extract text from paragraphs
    texts = [p['text'] for p in paragraphs]

    # Generate embeddings
    embeddings = embed_text(texts)

    # Create a FAISS index (L2 distance)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))

     # Save to in-memory maps
    index_map[doc_id] = index
    meta_map[doc_id] = paragraphs

    # Save to disk
    save_index_and_meta(doc_id, index, paragraphs)


 #Load all saved FAISS indices and metadata from disk into memory.
def load_all_indices():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR, exist_ok=True)
    files = os.listdir(SAVE_DIR)
    if not files:
        print("[INFO] No embeddings found. Skipping load.")
        return

    for file in files:
        if file.endswith(".index"):
            doc_id = int(file.replace(".index", ""))
            index_path = os.path.join(SAVE_DIR, file)
            meta_path = os.path.join(SAVE_DIR, f"{doc_id}_meta.pkl")

              # Load FAISS index
            index = faiss.read_index(index_path)

             # Load metadata
            with open(meta_path, "rb") as f:
                meta = pickle.load(f)

             # Populate in-memory maps
            index_map[doc_id] = index
            meta_map[doc_id] = meta

#Perform semantic search on a single document's paragraphs.
def search_similar_paragraphs(doc_id,query,top_k=3):
    if doc_id  not in index_map:
        return []
    query_vec = embed_text([query])  #Encode the query text into vactors
    D,I = index_map[doc_id].search(np.array(query_vec).astype('float32'),top_k)
    result = [meta_map[doc_id][i] for i in I[0]]
    return result

#Check if a FAISS index exists for a given document ID.
def index_exists(doc_id):
    return doc_id in index_map

#Get all document IDs currently loaded in memory.
def get_all_doc_ids():
    return list(index_map.keys())

#Perform semantic search across multiple documents.
def cross_document_search(doc_ids,query,top_k=3):
    all_matches = []
    for doc_id in doc_ids:
        if doc_id in index_map:
            matches = search_similar_paragraphs(doc_id,query,top_k)
            for match in matches:
                match["doc_id"] = doc_id
                all_matches.append(match)
    return all_matches


