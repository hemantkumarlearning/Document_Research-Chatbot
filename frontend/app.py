# Import necessary libraries
import streamlit as st 
import requests
import os
import re

# Get backend URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL")

# Set the app title
st.title("Document Research Assistant")

# Sidebar menu options
menu = ["Upload", "Documents", "Chat", "Themes"] 
choice = st.sidebar.selectbox("Menu", menu)

# Helper function to bold theme and document references in the response text
def bold_theme_headings(text):
    text= re.sub(r"(Theme \d+ - [^\n:]+:)", r"**\1**\n", text)
    text = re.sub(r"\b(Documents? \d+(?: and \d+)*(?:,? \d+)*)", r"**\1**", text)
    return text

#Upload Page
if choice == "Upload": 
    uploaded_file = st.file_uploader("Upload a document") 
    if uploaded_file: 
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)} 
        res = requests.post(f"{BACKEND_URL}/upload", files=files) 
        if res:
            st.markdown("## 📄File Uploaded Successfully ")

#Document page
elif choice == "Documents": 
    res = requests.get(f"{BACKEND_URL}/documents") 
    docs = res.json()
    st.markdown("### 📄 Uploaded Documents")
    for doc in docs:
        st.markdown(f"- **ID:** `{doc['doc_id']}` | **Name:** `{doc['name']}`")
    
#Chat page
elif choice == "Chat": 
    doc_id = st.text_input("Enter Document ID")
    question = st.text_input("Ask a question") 
    if doc_id and question: 
        res = requests.post(f"{BACKEND_URL}/chat", json={"doc_id":doc_id, "question": question}) 
        
        if res.status_code == 200:
            response_text = res.text
            formated_text = response_text.replace("\\n","\n")
            formatted = formated_text.replace("Document ID:", "**Document ID:**")
            format = formatted.replace("Citation:", "\n**Citation:**")
            final_text = format.replace("Extracted Answer:","\n**Extracted Answer:**")
            st.markdown(final_text)

#Theme page
elif choice == "Themes": 
    question = st.text_input("Ask question")
    if question:
        res = requests.post(f"{BACKEND_URL}/themes", json={"question":question}) 
        if res.status_code == 200:
            response_text = res.text
            formated_text = response_text.replace("\\n","\n")
            formatted_response = bold_theme_headings(formated_text)
            st.markdown(formatted_response)