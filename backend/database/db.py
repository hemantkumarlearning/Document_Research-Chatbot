# Import necessary modules
from sqlalchemy import create_engine, Column, Integer, String, Text,ForeignKey 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
import os

# Load database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


# Define the Document table/model
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique ID for the document
    name = Column(String)  # Name or title of the document
    paragraphs = relationship("Paragraph", back_populates="document")  # One-to-many relationship to Paragraphs


# Define the Paragraph table/model
class Paragraph(Base):
    __tablename__ = "paragraphs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique ID for the paragraph
    doc_id = Column(Integer, ForeignKey("documents.id"))  # Foreign key linking to the Document
    page = Column(Integer)  # Page number in the original document
    para = Column(Integer)  # Paragraph number within the page
    text = Column(Text)  # The paragraph text itself
    
    document = relationship("Document", back_populates="paragraphs")  # Reference back to the parent Document


# Function to initialize the database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)


# Store a document and its associated paragraphs in the database
def store_document(name, paras):
    db = SessionLocal()  # Create a new database session
    doc = Document(name=name)  # Create a new Document object
    db.add(doc)  # Add document to the session
    db.flush()  # Flush to assign the document an ID before using it in paragraphs

    for para in paras:
        paragraph = Paragraph(
            doc_id=doc.id,  # Link paragraph to the document
            page=para['page'],
            para=para['para'],
            text=para['text']
        )
        db.add(paragraph)  # Add paragraph to the session

    db.commit()  # Commit all changes to the database
    db.close()  # Close the session


# Retrieve a list of all documents (id and name)
def get_all_documents():
    db = SessionLocal()
    docs = db.query(Document).all()  # Fetch all document entries
    result = [{"doc_id": d.id, "name": d.name} for d in docs]  # Format results
    db.close()
    return result


# Retrieve a specific document by ID
def get_document(doc_id):
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == doc_id).first()  # Fetch document by ID
    result = {"doc_id": doc.id, "name": doc.name}  # Format result
    db.close()
    return result


# Retrieve all paragraphs for a specific document ID
def get_paragraphs(doc_id):
    db = SessionLocal()
    paras = db.query(Paragraph).filter(Paragraph.doc_id == doc_id).all()  # Fetch paragraphs by doc ID
    result = [{"page": p.page, "para": p.para, "text": p.text} for p in paras]  # Format result
    db.close()
    return result

