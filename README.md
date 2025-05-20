## Document-Aware Chatbot
A fully functional, web-based AI-powered chatbot that allows users to upload documents (PDF, DOCX, Images), extract and store text in a database, and then chat or query these documents using semantic search powered by sentence-transformers, FAISS, and Groq LLaMA models. The application also supports theme-based querying across documents.

## Features

- Upload PDF, DOCX, and Image files.

- Extract text, page, and paragraph-level metadata.

- Store data in PostgreSQL using SQLAlchemy.

- Generate sentence embeddings using Hugging Face's sentence-transformers.

- Index data with FAISS for semantic search.

- Search using natural language questions with document-specific context.

- Thematic search across all uploaded documents.

- Chat responses powered by Groq LLaMA models.

- Web UI built with Streamlit.

## Technologies Used

- FastAPI – API development

- Streamlit – Web UI for interacting with backend

- PyMuPDF, python-docx, pytesseract – Document text extraction

- SQLAlchemy + PostgreSQL – Data storage

- FAISS – Vector indexing

- Hugging Face Sentence Transformers – Embedding generation

- Groq LLaMA – Natural language response generation

## Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/hemantkumarlearning/hemant-kumar-wasserstoff-AiInternTask.git
cd hemant-kumar-wasserstoff-AiInternTask
```

### 2. Backend Setup

```
python -m venv venv
source venv/Scripts/activate
cd backend
pip install -r requirements.txt
```

Create a .env file with your database and API keys:
```
DATABASE_URL=postgresql://username:password@localhost:5432/yourdb
GROQ_API_KEY=your_groq_api_key
DATABASE_URL = your_postgresql_database_url
```

Run the FastAPI server:
```
uvicorn main:app --reload
```

### 3. Frontend Setup
```
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```

## Demo

## Core Functionalities Explained

- Document Parsing: PDFs are parsed using PyMuPDF, DOCX via python-docx, and images through OCR (pytesseract).

- Database Storage: Paragraph and page-level data with metadata is stored in PostgreSQL.

- Embedding & Indexing: Text is converted to vectors using Hugging Face models and indexed with FAISS.

- Document Chat: A user can input a document ID and a question to receive an answer contextualized to that specific document.

- Thematic Search: Search across all indexed documents to extract relevant themes from various sources.

- Citation Support: Each answer includes the source document, page, and paragraph number.
