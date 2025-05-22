import requests
import os

# Load groq api key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# return document id, extracted answer and citation from document id and matched paragraphs
def query_llm(doc_id,matched_paragraphs): 
    context = "\n\n".join([p['text'] for p in matched_paragraphs]) #Join all paragraphs text into a single text
    citation = [(p['page'],p['para']) for p in matched_paragraphs] #Extract all page and paragraphs
    prompt = f"""You are given text extracted from documents and their citations (page and paragraph numbers).

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
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    ) 
    return response.json()["choices"][0]["message"]["content"]