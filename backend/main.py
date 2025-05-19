from fastapi import FastAPI 
from backend.services.faiss_service import load_all_indices
from backend.routers import upload, documents,chat,theme
from backend.database.db import init_db
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router) 
app.include_router(documents.router) 
app.include_router(chat.router) 
app.include_router(theme.router)

@app.on_event("startup")
def startup_event():
    load_all_indices()
    init_db()
    