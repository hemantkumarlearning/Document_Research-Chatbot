# Import necessary modules and functions
from fastapi import APIRouter, UploadFile, File 
from backend.services.ocr_service import extract_text 
from backend.database.db import store_document

# Create a router instance to define API routes
router = APIRouter()

#Upload file(pdf,docx)
@router.post("/upload") 
async def upload_file(file: UploadFile = File(...)): 

    #Extract page,paragraph and text from uploaded file
    paragraphs = extract_text(file)

    #Store this paragraphs with file name in database
    store_document(file.filename,paragraphs)
    return {"status":"uploaded"}