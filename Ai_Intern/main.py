"""
FastAPI Application
REST API endpoint for the RAG question-answering system
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from qa_pipeline import RAGPipeline
from evaluation import comprehensive_evaluation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Knowledge Helper",
    description="RAG-based Question Answering System",
    version="1.0.0"
)

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()


# Request/Response models
class QuestionRequest(BaseModel):
    question: str
    top_k: Optional[int] = None
    use_summarization: Optional[bool] = False
    evaluate: Optional[bool] = False


class QuestionResponse(BaseModel):
    answer: str
    sources: list
    confidence: float
    num_sources: int
    evaluation: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str
    vector_db_loaded: bool


# API Endpoints
@app.get("/", tags=["General"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Knowledge Helper API",
        "version": "1.0.0",
        "endpoints": {
            "POST /ask": "Ask a question",
            "GET /health": "Check API health",
            "POST /process": "Process documents"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Check if the API is running and vector DB is loaded."""
    return {
        "status": "healthy",
        "vector_db_loaded": rag_pipeline.vector_db_loaded
    }


@app.post("/ask", response_model=QuestionResponse, tags=["QA"])
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an answer using RAG.
    
    - **question**: The question to ask
    - **top_k**: Number of chunks to retrieve (optional)
    - **use_summarization**: Whether to summarize retrieved chunks (optional)
    - **evaluate**: Whether to include evaluation metrics (optional)
    """
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get answer from RAG pipeline
        result = rag_pipeline.ask(
            question=request.question,
            top_k=request.top_k,
            use_summarization=request.use_summarization
        )
        
        # Add evaluation if requested
        evaluation = None
        if request.evaluate and result.get("sources"):
            evaluation = comprehensive_evaluation(
                query=request.question,
                retrieved_texts=result["sources"],
                answer=result["answer"]
            )
        
        response = QuestionResponse(
            answer=result.get("answer", "No answer available"),
            sources=result.get("sources", []),
            confidence=result.get("confidence", 0.0),
            num_sources=result.get("num_sources", len(result.get("sources", []))),
            evaluation=evaluation
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/process", tags=["Processing"])
async def process_documents(force_rebuild: bool = False):
    """
    Process documents in the data directory.
    
    - **force_rebuild**: Whether to rebuild the vector DB even if it exists
    """
    try:
        rag_pipeline.process_documents(force_rebuild=force_rebuild)
        return {
            "status": "success",
            "message": "Documents processed successfully",
            "vector_db_loaded": rag_pipeline.vector_db_loaded
        }
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

