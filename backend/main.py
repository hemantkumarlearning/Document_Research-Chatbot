from fastapi import FastAPI 
# from backend.services.faiss_service import load_all_indices
from backend.routers import upload, documents,chat,theme
from backend.database.db import init_db
from fastapi.middleware.cors import CORSMiddleware


# Create the FastAPI application instance
app = FastAPI()

# Add CORS middleware to allow requests from any origin
# This is useful when the frontend and backend are hosted on different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define startup event to run initial setup tasks
app.include_router(upload.router) 
app.include_router(documents.router) 
app.include_router(chat.router) 
app.include_router(theme.router)

@app.on_event("startup")
def startup_event():
    # load_all_indices()
    init_db()
    