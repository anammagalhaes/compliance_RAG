from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredHTMLLoader
)
from pathlib import Path

def load_documents(directory):
    docs = []
    path = Path(directory)

    for file in path.rglob("*"):
        if file.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(file)).load())
        elif file.suffix.lower() == ".txt":
            docs.extend(TextLoader(str(file)).load())
        elif file.suffix.lower() == ".csv":
            docs.extend(CSVLoader(file_path=str(file), encoding='utf-8').load())
        elif file.suffix.lower() in [".html", ".htm"]:
            docs.extend(UnstructuredHTMLLoader(str(file)).load())
    
    return docs

