# Import necessary modules and functions
from fastapi import APIRouter 
from backend.database.db import get_all_documents,get_document

# Create a router instance to define API routes
router = APIRouter()

#Get all documents
@router.get("/documents") 
def list_documents(): 

    #This method will return all documents stored in the database
    return get_all_documents()

#Get document by id
@router.get("/document/{doc_id}") 
def document_detail(doc_id:str):

    #This will return the specific document by id 
    return get_document(doc_id)