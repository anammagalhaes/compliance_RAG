from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend import build_qa_chain

app = FastAPI(
    title="Dow Jones AI Compliance Copilot API",
    version="1.0"
)

# Build the QA chain on startup (reuses your existing build_qa_chain)
qa_chain = build_qa_chain("data/index")

class QARequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    answer: str

#@app.get("/health")
#def health_check():
#    return {"status": "ok", "message": "API is running."}

@app.post("/qa", response_model=QAResponse)
def ask_question(req: QARequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")
    try:
        result = qa_chain.invoke({"query": question})
        return QAResponse(answer=result.get("result", ""))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
