from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import src.parser as parser


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

#NOTE!!!! THE parser.py module is not being used in the pipeline.
# It is only used for the initial POC to load documents and embed them.

# # Ideal usage (production):
# from parser import load_documents, clean_and_parse
# from embedder import embed_and_store
#
# raw_docs    = load_documents("data/raw")
# cleaned_docs = clean_and_parse(raw_docs)
# embed_and_store(cleaned_docs, "data/index")
#
# # Emergency workaround (POC/demo on local laptop):
# # Due to limited RAM/CPU/GPU and no cloud infrastructure available,
# # the current build process bypasses the cleaning step.
# from parser import load_documents
# from embedder import embed_and_store
#
# raw_docs = load_documents("data/raw")
# embed_and_store(raw_docs, "data/index")