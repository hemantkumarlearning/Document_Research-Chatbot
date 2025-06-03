from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 
import os

# Load groq api key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# return document id, extracted answer and citation from document id and matched paragraphs
def query_llm(doc_id,matched_paragraphs): 
    context = "\n\n".join([p['text'] for p in matched_paragraphs]) #Join all paragraphs text into a single text
    citation = [(p['page'],p['para']) for p in matched_paragraphs] #Extract all page and paragraphs
    prompt_template = PromptTemplate(
        input_variables=["doc_id", "context", "citation"],
        template="""You are given text extracted from documents and their citations (page and paragraph numbers).

Document ID:  
{doc_id}   
Extracted Answer:  
<Your summary here>  
Citation:  
Page X,  
Para Y  
Page Z,  
Para A

Use line breaks exactly as shown. Only include the summary and the list of citations. Do not include any explanation, commentary and preamble.

Here is the text to summarize:
{context}

Citations:
{citation}
"""
    )
    llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name='llama-3.3-70b-versatile') 
    chain = LLMChain(prompt=prompt_template, llm=llm)
    response = chain.run({
        "doc_id": doc_id,
        "context": context,
        "citation": citation
    })

    return response.strip()

