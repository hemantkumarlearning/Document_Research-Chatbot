from fastapi import APIRouter, UploadFile, File 
from backend.services.ocr_service import extract_text 
from backend.database.db import store_document


router = APIRouter()

@router.post("/upload") 
async def upload_file(file: UploadFile = File(...)): 
    paragraphs = extract_text(file)
    store_document(file.filename,paragraphs)
    return {"status":"uploaded"}