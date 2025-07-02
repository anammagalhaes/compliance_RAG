import os
from parser import load_documents
from embedder import embed_and_store

def build_vector_store(docs_path, index_path):
    print(f"===Loading documents from {docs_path} ===")
    documents = load_documents(docs_path)
    print(f"=== Loaded {len(documents)} documents ===")

    print("=== Adding new documents to vector store (index) ===")
    embed_and_store(documents, index_path)
    print("=== Index updated successfully. ===")

if __name__ == "__main__":
    DOCS_DIR = "data/raw"
    INDEX_DIR = "data/index"
    build_vector_store(DOCS_DIR, INDEX_DIR)
