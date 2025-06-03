from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 
import os

#Load groq api key from environmental variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Return all synthesize themes with document id which is semantic related to the question
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

        prompt_template = PromptTemplate(
        input_variables=["question", "synthesis_input"],
        template="""
You are an expert legal analyst. You are given a user question and relevant excerpts from multiple documents. 
Your task is to synthesize coherent and distinct themes from the provided information.

- Clearly identify multiple themes if they exist.
- Support each theme with references to document IDs.
- Return the final response in a professional and structured format.

Question: {question}

Relevant Information:
{synthesis_input}

Respond in the following format:
Theme 1 - [Theme Title]:
Documents number indicate that ...

Theme 2 - [Theme Title]:
Document number suggests that ...
"""
    )
    llm = ChatGroq(
        temperature=0,
        groq_api_key=GROQ_API_KEY,
        model_name='llama-3.3-70b-versatile'
    )

    # Set up the chain
    chain = LLMChain(prompt=prompt_template, llm=llm)

    # Run the chain with inputs
    response = chain.run({
        "question": question,
        "synthesis_input": synthesis_input
    })

    return response.strip()

