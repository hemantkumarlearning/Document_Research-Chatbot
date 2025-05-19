import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def synthesize_themes_all_documents(matches,question):
    grouped_by_doc = {}
    for match in matches:
        doc_id = match["doc_id"]
        text = match["text"]
        grouped_by_doc.setdefault(doc_id, []).append(text)

    synthesis_input = ""
    for doc_id, texts in grouped_by_doc.items():
        combined_text = " ".join(texts)
        synthesis_input += f"\nDocument {doc_id}:\n{combined_text}\n"

        prompt = f"""You are an expert legal analyst. You are given a user question and relevant excerpts from multiple documents. 
Your task is to synthesize coherent and distinct themes from the provided information.
- Clearly identify multiple themes if they exist.
- Support each theme with references to document IDs.
- Return the final response in a professional and structured format.

Question: {question}

Relevant Information:
{synthesis_input}

Respond in the following format:
Theme 1 – [Theme Title]:
Documents (DOC001, DOC002) indicate that ...
Theme 2 – [Theme Title]:
DOC003 suggests that ...
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

