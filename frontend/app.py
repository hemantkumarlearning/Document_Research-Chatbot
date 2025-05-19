import streamlit as st 
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL")
st.title("Document Research Assistant")

menu = ["Upload", "Documents", "Chat", "Themes"] 
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Upload": 
    uploaded_file = st.file_uploader("Upload a document") 
    if uploaded_file: 
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)} 
        res = requests.post("{BACKEND_URL}/upload", files=files) 
        if res:
            st.markdown("## 📄File Uploaded Successfully ")

elif choice == "Documents": 
    res = requests.get("{BACKEND_URL}/documents") 
    docs = res.json()
    st.markdown("### 📄 Uploaded Documents")
    for doc in docs:
        st.markdown(f"- **ID:** `{doc['doc_id']}` | **Name:** `{doc['name']}`")
    

elif choice == "Chat": 
    doc_id = st.text_input("Enter Document ID")
    question = st.text_input("Ask a question") 
    if doc_id and question: 
        res = requests.post("{BACKEND_URL}/chat", json={"doc_id":doc_id, "question": question}) 
        
        if res.status_code == 200:
            response_text = res.text
            formated_text = response_text.replace("\\n","\n")
            st.text(formated_text)

elif choice == "Themes": 
    question = st.text_input("Ask question")
    if question:
        res = requests.post("{BACKEND_URL}/themes", json={"question":question}) 
        if res.status_code == 200:
            response_text = res.text
            formated_text = response_text.replace("\\n","\n")
            st.text(formated_text)