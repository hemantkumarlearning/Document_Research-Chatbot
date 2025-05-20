from sqlalchemy import create_engine, Column, Integer, String, Text,ForeignKey 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base = declarative_base()

class Document(Base): 
    __tablename__ = "documents" 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String) 
    paragraphs = relationship("Paragraph",back_populates="document")

class Paragraph(Base): 
    __tablename__ = "paragraphs" 
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("documents.id"))
    page = Column(Integer)
    para = Column(Integer)
    text = Column(Text)
    document = relationship("Document",back_populates="paragraphs") 

def init_db():
    Base.metadata.create_all(bind=engine)

def store_document(name, paras): 
    db = SessionLocal() 
    doc = Document(name=name)
    db.add(doc)
    db.flush()  
        
    for para in paras:
        paragraph = Paragraph(
            doc_id=doc.id,
            page=para['page'],
            para=para['para'],
            text=para['text']
        )
        db.add(paragraph)
        db.commit()
        db.close()
    
def get_all_documents(): 
    db = SessionLocal() 
    docs = db.query(Document).all()
    result = [{"doc_id":d.id,"name":d.name} for d in docs]
    db.close()
    return result

def get_document(doc_id): 
    db = SessionLocal() 
    doc = db.query(Document).filter(Document.id == doc_id).first()
    result = {"doc_id":doc.id,"name":doc.name}
    db.close()
    return result

def get_paragraphs(doc_id): 
    db = SessionLocal() 
    paras = db.query(Paragraph).filter(Paragraph.doc_id == doc_id).all()
    result = [{"page":p.page,"para":p.para,"text":p.text} for p in paras]
    db.close()
    return result

