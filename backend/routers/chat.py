# Import necessary modules and functions
from fastapi import APIRouter
from backend.services.faiss_service import embed_and_store, index_exists, search_similar_paragraphs
from backend.models.models import QueryRequest
from backend.services.llm_service import query_llm
from backend.database.db import get_paragraphs

# Create a router instance to define API routes
router = APIRouter()

@router.post("/chat") 
async def chat_with_docs(request: QueryRequest): 

     # Check if the FAISS index for the given document ID exists
    if not index_exists(request.doc_id):

        # If it doesn't exist, retrieve paragraphs for the document from the database
        paras = get_paragraphs(request.doc_id)

         # Generate embeddings for the paragraphs and store them in the FAISS index
        embed_and_store(request.doc_id,paras)

         # Search for paragraphs most similar to the question using the FAISS index
        matched = search_similar_paragraphs(request.doc_id,request.question)

        # Pass the matched paragraphs and document ID to the language model to get an answer
        answer = query_llm(request.doc_id,matched)

        return answer
    else:

         # If the FAISS index already exists, directly search for similar paragraphs
        matched = search_similar_paragraphs(request.doc_id,request.question)
        answer = query_llm(request.doc_id,matched)
        return answer