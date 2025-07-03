# Compliance RAG Copilot 

This project is a proof of concept for a modular Retrieval-Augmented Generation (RAG) system designed around compliance-related content. It simulates how Dow Jones could provide intelligent question-answering capabilities to B2B clients, giving natural language access to structured and unstructured regulatory data.

## Architecture Overview

```
compliance_rag/
├── api.py                 # FastAPI service exposing /qa endpoint
├── backend.py             # Q&A logic using retriever + LLM
├── main.py                # Local CLI pipeline runner
├── gradio_app.py          # Web interface (optional) - Next version
├── requirements.txt       # Python dependencies
├── data/
│   ├── raw/               # Compliance documents (PDF, HTML, CSV)
│   └── index/             # FAISS vector index
├── docs/
│   └── fetch_data.py      # Public document downloader
├── src/
│   ├── parser.py          # Parses and cleans documents
│   ├── embedder.py        # Embedding and indexing in FAISS
│   └── build_index.py     # Full indexing pipeline
├── AI_Compliance_Copilot.ipynb  # Notebook with explanation & demo
└── compliance_suggestion_questions.md  # Test question set
```

> In a production scenario, documents would come directly from internal systems or cloud storage, not scraped from public sites. This download simulation is used purely for prototyping.

## Initial Challenges

Several architectures were tested:

### Hugging Face LLMs (e.g. `flan-t5-base`)
- Required API tokens
- Produced 401 Unauthorized errors
- Some models not deployable via Inference Endpoints without paid plans

### Ollama for embeddings (`nomic-embed-text`)
- Too slow and heavy locally
- Resource limits caused frequent failures

## Final Working Setup

### Embeddings
- Model: `sentence-transformers/paraphrase-albert-small-v2`
- Source: Hugging Face (`langchain_community.embeddings.HuggingFaceEmbeddings`)
- Characteristics:
  - Runs locally without tokens
  - Fast and lightweight

### LLM
- Model: `tinyllama`
- Source: Ollama
- Characteristics:
  - Offline, no rate limits
  - Lightweight for prototyping

> **Note:** TinyLLaMA is limited compared to GPT-4 but sufficient for POC.

## Installation & Setup

### 1. Create a virtual environment

```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
``` 

### 3. Install Ollama and pull the model

```bash
# https://ollama.com
ollama run tinyllama
```

## Step 1: Prepare and Index Documents

### Download sample documents

```bash
python docs/fetch_data.py
```

### Build the FAISS index

**Preferred (with cleaning):**
```bash
python - <<EOF
from src.parser import load_documents, clean_and_parse
from src.embedder import embed_and_store
raw = load_documents("data/raw")
cleaned = clean_and_parse(raw)
embed_and_store(cleaned, "data/index")
EOF
```

**POC Shortcut (no cleaning):**
```bash
python - <<EOF
from src.parser import load_documents
from src.embedder import embed_and_store
raw = load_documents("data/raw")
embed_and_store(raw, "data/index")
EOF
```

### Inspect the index

```bash
python inspect_index.py
```

## Step 2: Run Locally via CLI or Notebook

### CLI Mode

```bash
python main.py
```

### Notebook Demo
Open `AI_Compliance_Copilot.ipynb` to run step-by-step in Jupyter, including example questions and source-cited answers.

## Step 3: API Usage

This section describes how to launch and interact with the FastAPI service.

### 1. Install FastAPI & Uvicorn

```bash
pip install fastapi uvicorn[standard]
```

### 2. Start the API server

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 4. Query the `/qa` Endpoint
Use **POST** with JSON body:

```bash
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{ "question": "How are cryptocurrency mixers used in ransomware schemes?" }'
```

Expected response:
```json
{ "answer": "<source-cited answer>" }
```

Or in **Postman**:
- Method: POST  
- URL: `http://localhost:8000/qa`  
- Body → Raw → JSON:
  ```json
  { "question": "What are the risks associated with cryptocurrency mixers?" }
  ```

## Design Principles

- **LLM-agnostic**: Swap between Ollama, Hugging Face, OpenAI
- **Modular**: Fetching, parsing, indexing, querying separated
- **Scalable**: Add more docs to `data/raw`, re-index, or in production use data from cloud storage and with differents types

## License

Publicly accessible documents only; intended for demonstration. Images and scanned tables are not indexed.


