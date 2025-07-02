# Compliance RAG System – Dow Jones B2B POC

This project is a proof of concept for a modular Retrieval-Augmented Generation (RAG) system designed around compliance-related content. It simulates how Dow Jones could provide intelligent question-answering capabilities to B2B clients, giving natural language access to structured and unstructured regulatory data.

## Architecture Overview

```
compliance_rag/
├── main.py                # CLI interface to ask questions
├── gradio_app.py          # Web interface (optional)
├── requirements.txt       # Python dependencies
├── data/
│   ├── raw/               # Compliance documents (PDF, HTML, CSV)
│   └── index/             # FAISS vector index
├── docs/
│   └── fetch_data.py      # Public document downloader
├── src/
│   ├── parser.py          # Parses and cleans documents
│   ├── embedder.py        # Embeds documents and stores FAISS
│   ├── build_index.py     # Full indexing pipeline
│   └── qa.py              # Q&A logic using retriever + LLM
├── notebooks/
│   └── final_walkthrough.ipynb  # Optional notebook with full explanation
```

> In a production scenario, documents would come directly from Dow Jones internal systems or cloud buckets, not scraped from the internet. This download simulation is used here purely for prototyping.

## Initial Challenges

Several architectures were tested:

### Hugging Face LLMs (e.g. `flan-t5-base`)
- Required API tokens
- Produced 401 Unauthorized errors, even with valid tokens
- Some models not deployable via Inference Endpoints without paid plans

### Ollama for embeddings (`nomic-embed-text`)
- Too slow and heavy for local usage
- Often failed due to large download size or resource limits

## Final Working Setup

The solution that worked best was:

### Embeddings
- Model: `sentence-transformers/paraphrase-albert-small-v2`
- Source: Hugging Face (via `langchain_community.embeddings.HuggingFaceEmbeddings`)
- Why it worked:
  - Runs locally
  - Does not require API token
  - Fast and lightweight

### LLM
- Model: `tinyllama`
- Source: Ollama (runs locally)
- Why it worked:
  - Offline
  - Lightweight
  - No rate limits or quotas
  - Solved issues with Hugging Face's hosted inference

> Note: TinyLLaMA is very limited compared to GPT-4, but sufficient for basic prototyping.

## Installation & Setup

### 1. Create a virtual environment

```bash
python -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama and pull the model

```bash
# Install from https://ollama.com
ollama run tinyllama
```

## Step 1: Populate Your Document Base

### Download compliance-related documents

```bash
python docs/fetch_data.py
```

Some downloads may fail due to external site restrictions (403, 404, or connection errors). In such cases, files were added manually. In a production scenario, these files would reside in authenticated internal storage, not scraped from the public web.

### Build the semantic index

```bash
python src/build_index.py
```

This loads all documents from `data/raw/`, splits them, creates embeddings, and stores them in `data/index/`.

### Inspect the current FAISS index

You can quickly inspect what content was embedded using the utility below:

```bash
python inspect_index.py
```

This will list the text content (first 300 chars) of each embedded document currently present in the vector store.

## Step 2: Ask Questions via CLI

```bash
python main.py
```

Example questions:

- “What is the most recent FATF recommendation?”
- “Was Tesla mentioned in any OFAC sanctions?”
- “What companies were involved in FinCEN advisories?”

In a real deployment, questions could be tailored to each client's business data—assuming the proper documents were ingested.

## Optional: Web Interface (Gradio)

```bash
python gradio_app.py
```

Opens a browser-based chat UI for the same question-answering system.

## Current Models Used

| Component     | Model                                           | Source        | Token Required |
|---------------|--------------------------------------------------|---------------|----------------|
| Embeddings    | sentence-transformers/paraphrase-albert-small-v2 | Hugging Face  | No             |
| LLM           | tinyllama                                       | Ollama        | No             |

These can be swapped in `app.py` and `embedder.py` for more powerful models like GPT-4 (via OpenAI API).

## Design Principles

- **LLM-Agnostic**: Switch between Ollama, Hugging Face, or OpenAI easily
- **Separation of concerns**: Fetching, parsing, indexing, and querying in clean modules
- **Scalable**: Just drop more files in `data/raw/` and rebuild the index
- **Prototyping-friendly**: Uses public data and minimal infra requirements

## License

This proof of concept uses only public, freely accessible documents and is intended solely for demonstration purposes.

Only the textual content of documents is embedded. Images, scanned tables, or OCR content are not indexed.