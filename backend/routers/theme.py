# Import necessary modules and functions
from fastapi import APIRouter 
from backend.services.faiss_service import cross_document_search, get_all_doc_ids
from backend.services.theme_service import synthesize_themes_all_documents
from backend.models.models import ThemeSynthesisRequest

# Create a router instance to define API routes
router = APIRouter()

#This will return all semantic related paragraphs with themes and doc_id
@router.post("/themes") 
def get_themes(request:ThemeSynthesisRequest):

    #It will return all doc_id which is stored in faiss index
    doc_ids = get_all_doc_ids()

    #Search for paragraphs in all stored documents most similar to the question 
    matches = cross_document_search(doc_ids,request.question,top_k=5)

    #return the semantic related paragraphs with themes and document id
    result = synthesize_themes_all_documents(matches,request.question)

    return result