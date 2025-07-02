from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def embed_and_store(docs, index_path):
    print(" === Splitting documents ===")
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    docs_split = splitter.split_documents(docs)
    print(f"=== Split into {len(docs_split)} chunks ===")

    print(" === Initializing embedding model ===")
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-albert-small-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    print("=== Creating FAISS index ===")
    texts = [doc.page_content for doc in docs_split]
    metadatas = [doc.metadata for doc in docs_split]

    vectorstore = FAISS.from_texts(texts, embedding, metadatas=metadatas)

    os.makedirs(index_path, exist_ok=True)
    print(f"=== Saving FAISS index to: {index_path} ===")
    vectorstore.save_local(index_path)
    print("=== Index saved successfully ===")
