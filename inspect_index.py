from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def inspect_index(index_path="data/index", preview_chars=300):
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-albert-small-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)

    docs_summary = []
    for i, doc in enumerate(db.docstore._dict.values()):
        summary = {
            "doc_id": i + 1,
            "source": doc.metadata.get("source", "unknown"),
            "preview": doc.page_content[:preview_chars]
        }
        docs_summary.append(summary)

    return docs_summary
