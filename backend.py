from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Custom prompt to control model behavior
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

def build_qa_chain(index_path: str):
    print(f"Loading FAISS index from: {index_path}")

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-albert-small-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    print("=== Starting local LLM via Ollama ===")
    llm = Ollama(
        model="tinyllama",
        temperature=0.3,
        top_p=0.95,
        repeat_penalty=1.1
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )

    return qa_chain

def run_qa_app(index_path: str):
    qa_chain = build_qa_chain(index_path)

    print("=== System is ready. Ask your compliance questions below ===\n")

    while True:
        question = input("Your question (or type 'exit'): ")
        if question.lower() in ["exit", "quit"]:
            print("=== Session ended ===")
            break

        response = qa_chain.invoke({"query": question})
        print(f"\n=== Answer:\n{response['result']}\n")




# New function for notebook-based Q&A!!!! PROBLEEEEMMM
def ask_question(question, index_path="data/index"):
    qa_chain = build_qa_chain(index_path)
    response = qa_chain.invoke({"query": question})
    return response["result"]