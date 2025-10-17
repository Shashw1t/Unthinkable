# 🔍 Knowledge Base Search Engine

A powerful **RAG (Retrieval-Augmented Generation)** based search engine that allows you to upload documents and ask questions using AI-powered natural language processing.

Demo Video Link : 

## Overview

This Knowledge Base Search Engine implements a complete RAG pipeline that:
- **Ingests** multiple document formats (PDF, TXT, DOCX)
- **Processes** and chunks documents intelligently
- **Generates embeddings** using Sentence Transformers
- **Stores** vectors in ChromaDB for efficient retrieval
- **Retrieves** relevant context using semantic similarity search
- **Synthesizes** answers using LLM (OpenAI GPT or Anthropic Claude)
- **Presents** results through an intuitive web interface

## Features

### Document Processing
-  Support for PDF, TXT, and DOCX files
-  Intelligent text extraction and cleaning
-  Smart chunking with configurable overlap
-  Multiple file upload capability

### RAG Implementation
-  Sentence Transformers for embeddings generation
-  ChromaDB vector database for efficient storage
-  Semantic similarity search with configurable parameters
-  Context-aware retrieval with metadata tracking

### LLM Integration
-  OpenAI GPT-3.5/GPT-4 support
-  Anthropic Claude support
-  Configurable prompt engineering
-  Source citation in answers

### User Interface
-  Clean, modern web interface
-  Drag-and-drop file upload
-  Real-time query processing
-  Source document visualization
-  Statistics dashboard

### Backend API
-  RESTful API with FastAPI
-  CORS enabled for frontend integration
-  Comprehensive error handling
-  File size validation
-  Health check endpoints

## Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Frontend (HTML/CSS/JS)        │
│   - File Upload Interface       │
│   - Query Input                 │
│   - Results Display             │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   FastAPI Backend               │
│   - REST API Endpoints          │
│   - Request Validation          │
│   - Response Formatting         │
└────┬────────────────────────┬───┘
     │                        │
     ▼                        ▼
┌──────────────┐    ┌─────────────────┐
│  Document    │    │   RAG Engine    │
│  Processor   │    │                 │
│              │    │  - Embeddings   │
│ - Extract    │───▶│  - Vector DB    │
│ - Clean      │    │  - Similarity   │
│ - Chunk      │    │    Search       │
└──────────────┘    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   LLM Service   │
                    │                 │
                    │  - OpenAI GPT   │
                    │  - Anthropic    │
                    │  - Synthesis    │
                    └─────────────────┘
```

### Data Flow

1. **Document Ingestion**
   - User uploads documents via frontend
   - Backend validates file type and size
   - Document Processor extracts and cleans text
   - Text is chunked with overlap for context preservation

2. **Embedding & Storage**
   - RAG Engine generates embeddings using Sentence Transformers
   - Embeddings stored in ChromaDB with metadata
   - Vector index created for fast similarity search

3. **Query Processing**
   - User submits natural language query
   - Query converted to embedding
   - Semantic search retrieves top-k relevant chunks
   - Context assembled from retrieved documents

4. **Answer Generation**
   - Context and query sent to LLM
   - LLM synthesizes answer based on retrieved information
   - Answer returned with source citations
   - Results displayed in frontend

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 2GB free disk space
- Internet connection for downloading models

### Quick Start (Windows)

1. **Clone the repository**
```powershell
git clone <your-repo-url>
cd Unthinkable1
```

2. **Run the startup script**
```powershell
.\start.bat
```

This will automatically:
- Create a virtual environment
- Install all dependencies
- Set up configuration files
- Start the server

### Quick Start (Linux/Mac)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Unthinkable1
```

2. **Make the startup script executable and run**
```bash
chmod +x start.sh
./start.sh
```

### Manual Installation

1. **Create virtual environment**
```powershell
python -m venv venv
```

2. **Activate virtual environment**
```powershell
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment**
```powershell
# Copy the example env file
copy .env.example .env

# Edit .env with your API keys
notepad .env
```

5. **Run the application**
```powershell
python setup_and_run.py
```

## Configuration

### Environment Variables

Edit the `.env` file with your configuration:

```ini
# LLM API Keys (Required - choose one)
OPENAI_API_KEY=sk-your-openai-api-key-here
# ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# LLM Configuration
LLM_PROVIDER=openai          # Options: openai, anthropic
LLM_MODEL=gpt-3.5-turbo      # or gpt-4, claude-2, etc.

# Embedding Model (uses Sentence Transformers)
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Document Processing
CHUNK_SIZE=1000              # Characters per chunk
CHUNK_OVERLAP=200            # Overlap between chunks
MAX_FILE_SIZE_MB=10          # Maximum file size

# Retrieval Configuration
TOP_K_RESULTS=5              # Number of chunks to retrieve
SIMILARITY_THRESHOLD=0.3     # Minimum similarity score
```
## Usage

### Starting the Server

python setup_and_run.py

Or directly with uvicorn:
uvicorn main:app --host 0.0.0.0 --port 8000

### Accessing the Application
Open your browser and navigate to:
```
http://localhost:8000
```


## API Documentation

### Endpoints

#### `GET /`
Returns the frontend HTML interface.

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Knowledge Base Search Engine",
  "version": "1.0.0"
}
```

#### `POST /upload`
Upload and process documents.

**Request:** Multipart form data with files

**Response:**
```json
{
  "results": [
    {
      "filename": "document.pdf",
      "success": true,
      "num_chunks": 15,
      "message": "Successfully processed and indexed 15 chunks"
    }
  ]
}
```

#### `POST /query`
Query the knowledge base.

**Request:**
```json
{
  "query": "What is machine learning?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Machine learning is...",
  "query": "What is machine learning?",
  "sources": [
    {
      "text": "chunk content...",
      "metadata": {
        "filename": "ml_guide.pdf",
        "chunk_index": 3
      },
      "similarity": 0.89
    }
  ],
  "num_sources": 3,
  "model": "gpt-3.5-turbo"
}
```

#### `GET /stats`
Get knowledge base statistics.

**Response:**
```json
{
  "success": true,
  "total_chunks": 150,
  "collection_name": "knowledge_base"
}
```

#### `DELETE /clear`
Clear all documents from the knowledge base.

**Response:**
```json
{
  "success": true,
  "message": "Collection cleared successfully"
}
```

#### `GET /test-llm`
Test LLM connection.

**Response:**
```json
{
  "success": true,
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "message": "Connection successful"
}
```


## Project Structure

```
Unthinkable1/
│
├── frontend/
│   └── index.html              # Web interface
│
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── config.py                   # Configuration settings
├── document_processor.py       # Document ingestion & processing
├── rag_engine.py              # RAG implementation
├── llm_service.py             # LLM integration
├── main.py                    # FastAPI application
├── setup_and_run.py           # Setup script
├── requirements.txt           # Python dependencies
├── start.bat                  # Windows startup script
├── start.sh                   # Unix startup script
└── README.md                  # This file

# Generated during runtime:
├── uploaded_documents/         # Uploaded files storage
├── chroma_db/                 # Vector database
└── venv/                      # Virtual environment
```

## Technologies Used

### Backend
- **FastAPI** - Modern web framework for building APIs
- **Python 3.8+** - Programming language
- **Pydantic** - Data validation
- **Python-multipart** - File upload handling

### Document Processing
- **PyMuPDF (fitz)** - PDF text extraction
- **PyPDF2** - Backup PDF processing
- **python-docx** - DOCX file handling

### RAG & Embeddings
- **ChromaDB** - Vector database for embeddings storage
- **Sentence Transformers** - Embedding generation
- **LangChain** - RAG orchestration utilities

### LLM Integration
- **OpenAI API** - GPT-3.5/GPT-4 integration
- **Anthropic API** - Claude integration

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern gradients
- **Vanilla JavaScript** - Interactivity and API calls

### Development
- **Uvicorn** - ASGI server
- **python-dotenv** - Environment management

## Evaluation Criteria

This project addresses all evaluation focus areas:

### 1. Retrieval Accuracy
- Semantic similarity search using state-of-the-art Sentence Transformers
- Configurable similarity threshold to filter low-quality matches
- Intelligent text chunking with overlap for context preservation
- Top-K retrieval with adjustable parameters
- Source metadata tracking for traceability

### 2. Synthesis Quality
- Integration with leading LLMs (GPT-3.5/4, Claude)
- Carefully engineered prompts for accurate answers
- Context-aware answer generation
- Source citation in responses
- Handling of insufficient information scenarios

### 3. Code Structure
- Clean separation of concerns (Document Processing, RAG, LLM, API)
- Modular architecture for easy extension
- Type hints throughout for code clarity
- Comprehensive error handling
- Configuration management with Pydantic
- Well-documented functions and classes

### 4. LLM Integration
- Support for multiple LLM providers
- Flexible prompt engineering
- Efficient token usage
- Graceful error handling
- Connection testing capability
- Configurable model selection


Created by Shashwat as part of the Unthinkable assignment.
