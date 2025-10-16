from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from pathlib import Path

from config import settings
from document_processor import DocumentProcessor
from rag_engine import RAGEngine
from llm_service import LLMService

# Initialize FastAPI app
app = FastAPI(
    title="Knowledge Base Search Engine",
    description="RAG-based document search and question answering system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services - will be created after startup cleanup
doc_processor = None
rag_engine = None
llm_service = None  # Will be initialized on first query (lazy loading)

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """Clear the knowledge base on startup to start fresh."""
    global doc_processor, rag_engine
    
    print("[STARTUP] Starting fresh - clearing all previous data...")
    
    # Delete ChromaDB directory completely
    chroma_path = Path(settings.chroma_db_dir)
    if chroma_path.exists():
        shutil.rmtree(chroma_path)
        print(f"[STARTUP] Deleted ChromaDB directory: {settings.chroma_db_dir}")
    
    # Clear uploaded documents folder
    upload_path = Path(settings.upload_dir)
    if upload_path.exists():
        for file in upload_path.iterdir():
            if file.is_file():
                file.unlink()
        print(f"[STARTUP] Cleared uploaded documents folder: {settings.upload_dir}")
    
    # Now initialize services with clean slate
    doc_processor = DocumentProcessor()
    rag_engine = RAGEngine()
    print("[STARTUP] Services initialized with clean database")
    print("[STARTUP] Ready to accept new documents!")


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = None


class QueryResponse(BaseModel):
    answer: str
    query: str
    sources: List[dict]
    num_sources: int
    model: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend."""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Knowledge Base Search Engine</h1><p>API is running. Frontend not found.</p>"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Knowledge Base Search Engine",
        "version": "1.0.0"
    }


@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload and process documents.
    Supports: PDF, TXT, DOCX
    """
    global doc_processor, rag_engine
    
    if doc_processor is None or rag_engine is None:
        raise HTTPException(status_code=503, detail="Services not initialized yet. Please wait a moment.")
    
    results = []
    
    for file in files:
        try:
            # Validate file size
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            if file_size > settings.max_file_size_mb * 1024 * 1024:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": f"File size exceeds {settings.max_file_size_mb}MB limit"
                })
                continue
            
            # Save file
            file_path = os.path.join(settings.upload_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process document
            process_result = doc_processor.process_document(file_path, file.filename)
            
            if process_result["success"]:
                # Add to vector database
                chunks = process_result["chunks"]
                metadata = [
                    {
                        "filename": file.filename,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                    for i in range(len(chunks))
                ]
                
                add_result = rag_engine.add_documents(chunks, metadata)
                
                if add_result["success"]:
                    results.append({
                        "filename": file.filename,
                        "success": True,
                        "num_chunks": len(chunks),
                        "message": f"Successfully processed and indexed {len(chunks)} chunks"
                    })
                else:
                    results.append({
                        "filename": file.filename,
                        "success": False,
                        "error": f"Failed to add to database: {add_result.get('error')}"
                    })
            else:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": process_result.get("error")
                })
        
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results}


@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """
    Query the knowledge base and get an AI-generated answer.
    """
    global llm_service, rag_engine
    
    if rag_engine is None:
        raise HTTPException(status_code=503, detail="Services not initialized yet. Please wait a moment.")
    
    try:
        # Initialize LLM service if not already done
        if llm_service is None:
            try:
                llm_service = LLMService()
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to initialize LLM service: {str(e)}"
                )
        
        # Search for relevant documents
        search_results = rag_engine.search(
            query=request.query,
            top_k=request.top_k
        )
        
        if not search_results["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Search failed: {search_results.get('error')}"
            )
        
        retrieved_chunks = search_results["results"]
        
        if not retrieved_chunks:
            return QueryResponse(
                answer="I couldn't find any relevant information in the knowledge base to answer your question.",
                query=request.query,
                sources=[],
                num_sources=0,
                model=settings.llm_model
            )
        
        # Generate answer using LLM
        llm_result = llm_service.synthesize_answer(
            query=request.query,
            context_chunks=retrieved_chunks
        )
        
        if not llm_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Answer generation failed: {llm_result.get('error')}"
            )
        
        return QueryResponse(
            answer=llm_result["answer"],
            query=request.query,
            sources=retrieved_chunks,
            num_sources=len(retrieved_chunks),
            model=llm_result["model"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Get knowledge base statistics."""
    global rag_engine
    
    if rag_engine is None:
        return {"success": True, "total_chunks": 0, "collection_name": "knowledge_base"}
    
    stats = rag_engine.get_collection_stats()
    return stats


@app.delete("/clear")
async def clear_knowledge_base():
    """Clear all documents from the knowledge base."""
    global rag_engine
    
    if rag_engine is None:
        return {"success": True, "message": "Knowledge base already empty"}
    
    result = rag_engine.clear_collection()
    
    # Also clear uploaded files
    try:
        upload_dir = Path(settings.upload_dir)
        if upload_dir.exists():
            for file in upload_dir.iterdir():
                if file.is_file():
                    file.unlink()
    except Exception as e:
        pass
    
    return result


@app.get("/test-llm")
async def test_llm_connection():
    """Test LLM connection."""
    global llm_service
    
    try:
        if llm_service is None:
            llm_service = LLMService()
        
        result = llm_service.test_connection()
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
