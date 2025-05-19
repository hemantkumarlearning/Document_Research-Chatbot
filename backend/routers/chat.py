from fastapi import APIRouter
from backend.services.faiss_service import embed_and_store, index_exists, search_similar_paragraphs
from backend.models.models import QueryRequest
from backend.services.llm_service import query_llm
from backend.database.db import get_paragraphs

router = APIRouter()

@router.post("/chat") 
async def chat_with_docs(request: QueryRequest): 
    if not index_exists(request.doc_id):
        paras = get_paragraphs(request.doc_id)
        embed_and_store(request.doc_id,paras)
        matched = search_similar_paragraphs(request.doc_id,request.question)
        answer = query_llm(request.doc_id,matched)
        return answer
    else:
        matched = search_similar_paragraphs(request.doc_id,request.question)
        answer = query_llm(request.doc_id,matched)
        return answer