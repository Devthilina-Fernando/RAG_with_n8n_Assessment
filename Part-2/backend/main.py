from fastapi import FastAPI
from routers import qa, summary

app = FastAPI(
    title="Document RAG API",
    version="1.0",
    description="API for document-based Q&A and summarization using RAG"
)

app.include_router(qa.router, prefix="/api/qa", tags=["Q&A"])
app.include_router(summary.router, prefix="/api/summary", tags=["Summarization"])