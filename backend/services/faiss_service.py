import faiss
import numpy as np
import os
import pickle
from backend.services.embedding_service import embed_text


SAVE_DIR = "/var/data/embedding_store"

def save_index_and_meta(doc_id, index, meta):

    faiss.write_index(index, os.path.join(SAVE_DIR, f"{doc_id}.index"))
    
    with open(os.path.join(SAVE_DIR, f"{doc_id}_meta.pkl"), "wb") as f:
        pickle.dump(meta, f)

index_map={}
meta_map={}


def embed_and_store(doc_id,paragraphs):
    texts = [p['text'] for p in paragraphs]
    embeddings = embed_text(texts)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    index_map[doc_id] = index
    meta_map[doc_id] = paragraphs
    save_index_and_meta(doc_id, index, paragraphs)

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

            index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                meta = pickle.load(f)

            index_map[doc_id] = index
            meta_map[doc_id] = meta


def search_similar_paragraphs(doc_id,query,top_k=3):
    if doc_id  not in index_map:
        return []
    query_vec = embed_text([query])
    D,I = index_map[doc_id].search(np.array(query_vec).astype('float32'),top_k)
    result = [meta_map[doc_id][i] for i in I[0]]
    return result


def index_exists(doc_id):
    return doc_id in index_map


def get_all_doc_ids():
    return list(index_map.keys())


def cross_document_search(doc_ids,query,top_k=3):
    all_matches = []
    for doc_id in doc_ids:
        if doc_id in index_map:
            matches = search_similar_paragraphs(doc_id,query,top_k)
            for match in matches:
                match["doc_id"] = doc_id
                all_matches.append(match)
    return all_matches


