from fastapi import APIRouter 
from backend.services.faiss_service import cross_document_search, get_all_doc_ids
from backend.services.theme_service import synthesize_themes_all_documents
from backend.models.models import ThemeSynthesisRequest


router = APIRouter()

@router.post("/themes") 
def get_themes(request:ThemeSynthesisRequest):
    doc_ids = get_all_doc_ids()
    matches = cross_document_search(doc_ids,request.question,top_k=5)
    result = synthesize_themes_all_documents(matches,request.question)

    return result