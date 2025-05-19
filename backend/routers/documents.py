from fastapi import APIRouter 
from backend.database.db import get_all_documents,get_document

router = APIRouter()

@router.get("/documents") 
def list_documents(): 
    return get_all_documents()

@router.get("/document/{doc_id}") 
def document_detail(doc_id:str): 
    return get_document(doc_id)