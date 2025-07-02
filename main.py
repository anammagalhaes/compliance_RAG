from pathlib import Path
#from src.build_index import build_vector_store
from backend import run_qa_app
from dotenv import load_dotenv
load_dotenv()

INDEX_DIR = Path("data/index")
DOCS_DIR = Path("data/raw")

from backend import run_qa_app

INDEX_DIR = "data/index"

def main():
    run_qa_app(INDEX_DIR)

if __name__ == "__main__":
    main()
