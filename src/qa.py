from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Prompt refinado para controle do comportamento do modelo
QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful compliance assistant.
Answer the question below using only the provided context.
If you don't know the answer based on the context, say:
"I’m sorry, I couldn't find information about that based on the current documents."

Context:
{context}

Question:
{question}
"""
)

def ask_question(question, retriever, llm):
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )
    result = qa.invoke({"query": question})
    return result['result']
