from pydantic import BaseModel

class QueryRequest(BaseModel):
    doc_id:str
    question:str

class ThemeSynthesisRequest(BaseModel):
    question:str