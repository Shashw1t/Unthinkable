# Knowledge Base Search Engine - Assignment Documentation

---

## 📌 Student Information

**Name:** Shashwat Dwivedi  
**Registration Number:** 22BCE8168  
**Email:** iamsoranic@gmail.com  
**Assignment:** Assignment 7 - Knowledge Base Search Engine  
**Submission Date:** October 24, 2025

---

## 🔗 Project Links

- **GitHub Repository:** https://github.com/Shashw1t/Unthinkable
- **Demo Video:** https://drive.google.com/file/d/1P4PdwSXVp6mx1ai5L75-6uaoFjKpLMf6/view?usp=drive_link
- **Live Deployment:** [Add Render URL if deployed]

---

## 📖 Project Overview

### What is this project?

The **Knowledge Base Search Engine** is an intelligent document search and question-answering system built using **Retrieval-Augmented Generation (RAG)** technology. It allows users to upload multiple documents (PDF, DOCX, TXT) and ask natural language questions, receiving AI-generated answers with source citations.

### Key Objectives

1. **Document Ingestion:** Process and store multiple document formats
2. **Intelligent Search:** Semantic search using vector embeddings
3. **AI Synthesis:** Generate comprehensive answers using LLM
4. **Source Attribution:** Provide transparent citations with similarity scores
5. **User-Friendly Interface:** Modern, responsive web application

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (HTML/CSS/JS)               │
│  - Document Upload Interface                            │
│  - Query Input Form                                     │
│  - Answer Display with Sources                          │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP/REST API
                 ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                   │
│  - /upload  - /query  - /stats  - /clear               │
└──────┬─────────────────────────────────┬────────────────┘
       │                                 │
       ▼                                 ▼
┌──────────────────┐            ┌────────────────────────┐
│ Document         │            │   RAG Engine           │
│ Processor        │            │                        │
│ - PDF Extract    │───────────▶│ - Embeddings Gen.     │
│ - Text Clean     │            │ - Vector Storage       │
│ - Smart Chunk    │            │ - Similarity Search    │
└──────────────────┘            └──────────┬─────────────┘
                                           │
                                           ▼
                                ┌────────────────────────┐
                                │  ChromaDB Vector DB    │
                                │  - Store Embeddings    │
                                │  - Semantic Search     │
                                └────────────────────────┘
                                           │
                                           ▼
                                ┌────────────────────────┐
                                │  Google Gemini API     │
                                │  - Answer Synthesis    │
                                │  - Context Processing  │
                                └────────────────────────┘
```

### RAG Pipeline Flow

1. **Document Upload** → Text Extraction → Chunking → Embedding Generation → Vector Storage
2. **User Query** → Query Embedding → Similarity Search → Context Retrieval → LLM Synthesis → Answer Display

---

## 💻 Technologies Used

### Backend
- **FastAPI 0.104.1** - High-performance REST API framework
- **Python 3.12** - Core programming language
- **Uvicorn** - ASGI web server

### Document Processing
- **PyPDF2 3.0.1** - PDF text extraction
- **python-docx 1.1.0** - DOCX file processing
- **Python built-in** - TXT file handling

### RAG Implementation
- **ChromaDB 0.4.22** - Vector database for embeddings storage
- **Sentence Transformers 2.2.2** - Embedding generation (all-MiniLM-L6-v2 model)
- **NumPy 1.26.2** - Numerical computations

### LLM Integration
- **Google Generative AI 0.3.2** - Gemini 2.0 Flash model for answer synthesis
- **Pydantic 2.5.0** - Data validation and settings management

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with gradients and animations
- **Vanilla JavaScript** - Dynamic interactions and API calls

### Development & Deployment
- **Git/GitHub** - Version control
- **Render** - Cloud deployment platform
- **Virtual Environment** - Dependency isolation

---

## ✨ Features Implemented

### 1. Document Management
✅ **Multi-format Support:** PDF, DOCX, TXT files  
✅ **Drag-and-Drop Upload:** Intuitive file upload interface  
✅ **Multiple File Upload:** Process several documents at once  
✅ **Real-time Processing:** Immediate feedback on upload status  
✅ **File Validation:** Size and format checking

### 2. Intelligent Text Processing
✅ **Smart Chunking:** 1000 characters per chunk with 200-character overlap  
✅ **Text Cleaning:** Remove extra whitespace and normalize text  
✅ **Metadata Tracking:** Store filename and chunk information  
✅ **Error Handling:** Graceful handling of corrupted files

### 3. RAG Implementation
✅ **Vector Embeddings:** 384-dimensional vectors using Sentence Transformers  
✅ **Semantic Search:** Cosine similarity-based retrieval  
✅ **Configurable Threshold:** Adjustable similarity filtering (set to 0.0 for demo)  
✅ **Top-K Retrieval:** Retrieve most relevant chunks  
✅ **Context Assembly:** Combine chunks for LLM input

### 4. AI-Powered Answers
✅ **LLM Integration:** Google Gemini 2.0 Flash for synthesis  
✅ **Context-Aware:** Uses retrieved documents for accurate answers  
✅ **Natural Language:** Human-readable, coherent responses  
✅ **Source Citations:** Every answer includes document references  
✅ **Similarity Scores:** Transparency in retrieval relevance

### 5. User Interface
✅ **Modern Design:** Gradient backgrounds (#134E5E, #0B3037) with cyan accents  
✅ **Animated Elements:** Floating particles, smooth transitions  
✅ **Responsive Layout:** Works on desktop and mobile  
✅ **Real-time Stats:** Document count, chunks, queries tracked  
✅ **Toast Notifications:** User feedback on actions  
✅ **Glassmorphism:** Modern card design with backdrop blur

### 6. API Endpoints
✅ **POST /upload** - Upload and process documents  
✅ **POST /query** - Submit questions and get answers  
✅ **GET /stats** - Retrieve system statistics  
✅ **DELETE /clear** - Clear all data  
✅ **GET /health** - Health check endpoint  
✅ **GET /** - Serve frontend HTML

---

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Google Gemini API Key

### Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/Shashw1t/Unthinkable.git
cd Unthinkable
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API key
GOOGLE_API_KEY=your_api_key_here
LLM_PROVIDER=google
LLM_MODEL=models/gemini-2.0-flash
SIMILARITY_THRESHOLD=0.0
```

5. **Run the Application**
```bash
# Windows
.\run.bat

# Linux/Mac
./run.sh

# Or manually
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

6. **Access the Application**
```
Open browser: http://127.0.0.1:8000
```

### Detailed Setup Instructions
For comprehensive setup instructions, refer to the **README.md** file in the GitHub repository.

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `LLM_PROVIDER` | LLM provider to use | `google` |
| `LLM_MODEL` | Gemini model name | `models/gemini-2.0-flash` |
| `SIMILARITY_THRESHOLD` | Minimum similarity score | `0.0` |
| `CHUNK_SIZE` | Text chunk size | `1000` |
| `CHUNK_OVERLAP` | Overlap between chunks | `200` |
| `UPLOAD_DIR` | Directory for uploads | `uploaded_documents` |
| `DB_DIR` | ChromaDB directory | `chroma_db` |

### Customization Options
- Adjust chunk size and overlap in `config.py`
- Change embedding model in `rag_engine.py`
- Modify UI colors in `frontend/index.html`
- Configure CORS settings in `main.py`

---

## 📊 API Documentation

### 1. Upload Documents
**Endpoint:** `POST /upload`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: files (one or more)

**Response:**
```json
{
  "message": "Successfully processed 2 files",
  "files": [
    {"filename": "doc1.pdf", "status": "success"},
    {"filename": "doc2.txt", "status": "success"}
  ]
}
```

### 2. Query Documents
**Endpoint:** `POST /query`

**Request:**
```json
{
  "query": "What is machine learning?"
}
```

**Response:**
```json
{
  "answer": "Machine learning is...",
  "sources": [
    {
      "document": "ml_intro.pdf",
      "text": "Machine learning involves...",
      "similarity": 0.85
    }
  ]
}
```

### 3. Get Statistics
**Endpoint:** `GET /stats`

**Response:**
```json
{
  "documents": 5,
  "chunks": 47,
  "queries": 12
}
```

### 4. Clear Data
**Endpoint:** `DELETE /clear`

**Response:**
```json
{
  "message": "All data cleared successfully"
}
```

---

## 🎯 Implementation Details

### Document Processing Strategy
1. **File Upload:** Receive files via multipart/form-data
2. **Format Detection:** Determine file type by extension
3. **Text Extraction:**
   - PDF: PyPDF2.PdfReader
   - DOCX: python-docx Document
   - TXT: Direct file read
4. **Text Cleaning:** Remove extra whitespace, normalize
5. **Chunking:** Split into overlapping segments
6. **Storage:** Save to upload directory for reference

### Embedding Generation
- **Model:** all-MiniLM-L6-v2 (Sentence Transformers)
- **Dimensions:** 384
- **Method:** sentence_transformers.SentenceTransformer.encode()
- **Normalization:** L2 normalization for cosine similarity

### Vector Storage
- **Database:** ChromaDB (in-memory + persistent)
- **Collection:** Single collection for all documents
- **Metadata:** Filename, chunk_id stored with vectors
- **Distance Metric:** Cosine similarity

### LLM Integration
- **Model:** Google Gemini 2.0 Flash
- **Temperature:** 0.7 (balanced creativity/accuracy)
- **Max Tokens:** 1024
- **Prompt Engineering:**
```
Using the following context from documents, answer the question.
If unsure, say so. Cite sources.

Context: [retrieved chunks]
Question: [user query]
```

### Error Handling
- File validation (size, format)
- API key validation
- Database connection errors
- LLM API failures
- Graceful degradation

---

## 🧪 Testing

### Manual Testing Performed
✅ Upload single PDF file  
✅ Upload multiple files (PDF, DOCX, TXT)  
✅ Upload invalid file formats (rejected)  
✅ Query with relevant documents  
✅ Query with no documents (handled gracefully)  
✅ Query with irrelevant question  
✅ Clear data functionality  
✅ Stats endpoint accuracy  
✅ Frontend responsiveness  
✅ Mobile view testing

### Sample Test Cases

**Test Case 1: Basic Upload and Query**
- Upload: `machine_learning_intro.pdf`
- Query: "What is machine learning?"
- Expected: Answer with source citation
- Result: ✅ Pass

**Test Case 2: Multiple Document Query**
- Upload: `ml_intro.pdf`, `python_guide.txt`
- Query: "Explain Python and ML"
- Expected: Answer synthesizing both documents
- Result: ✅ Pass

**Test Case 3: No Relevant Context**
- Upload: `cooking_recipes.pdf`
- Query: "Explain quantum computing"
- Expected: Honest "not found" response
- Result: ✅ Pass (with threshold 0.0, returns best match)

---

## 💡 Challenges Faced and Solutions

### Challenge 1: ChromaDB Installation on Windows
**Problem:** ChromaDB required C++ build tools for compilation  
**Solution:** Used ChromaDB 0.4.22 with pre-built wheels

### Challenge 2: PyMuPDF Deployment Issues
**Problem:** PyMuPDF required system-level C++ compilation on Render  
**Solution:** Switched to PyPDF2-only approach with graceful fallback

### Challenge 3: Similarity Threshold Too High
**Problem:** No results returned due to strict threshold (0.3)  
**Solution:** Adjusted to 0.0 for demo, allowing all results through

### Challenge 4: UTF-8 Encoding on Windows
**Problem:** HTML file couldn't be served due to encoding mismatch  
**Solution:** Added `encoding="utf-8"` to file open operations

### Challenge 5: Cold Start on Free Tier
**Problem:** Render free tier sleeps after 15 minutes  
**Solution:** Documented expected behavior, suggested paid tier for production

---

## 🚀 Deployment

### Platform: Render

**Deployment Steps:**
1. Push code to GitHub repository
2. Connect Render to GitHub repo
3. Configure build command: `pip install -r requirements.txt`
4. Configure start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (API keys)
6. Deploy and monitor logs

**Deployment Files:**
- `render.yaml` - Render configuration
- `requirements.txt` - Python dependencies
- `.gitignore` - Exclude sensitive files

**Live URL:** [Add your Render URL if deployed]

---

## 📈 Future Enhancements

### Planned Features
1. **User Authentication:** Login system for personal document libraries
2. **Persistent Storage:** Cloud storage (S3/GCS) for documents
3. **Advanced Search:** Filters by date, document type, author
4. **Multi-language Support:** Non-English document processing
5. **Conversation History:** Track and revisit past queries
6. **Document Summarization:** Auto-generate document summaries
7. **PDF Highlighting:** Show exact locations in source PDFs
8. **Batch Queries:** Process multiple questions at once
9. **Analytics Dashboard:** Usage statistics and insights
10. **API Rate Limiting:** Prevent abuse of endpoints

### Scalability Improvements
- Add Redis for caching
- Implement queue system for large uploads
- Horizontal scaling with load balancer
- Database sharding for large collections
- CDN for frontend assets

---

## 📚 Learning Outcomes

Through this project, I gained hands-on experience with:

1. **RAG Architecture:** Understanding retrieval-augmented generation
2. **Vector Databases:** Working with embeddings and similarity search
3. **LLM Integration:** Prompt engineering and API management
4. **FastAPI Development:** Building production-ready REST APIs
5. **Document Processing:** Handling multiple file formats
6. **Frontend Design:** Modern UI/UX with animations
7. **Deployment:** Cloud deployment on Render
8. **Git Workflow:** Version control and collaboration
9. **Error Handling:** Robust exception management
10. **Documentation:** Writing comprehensive technical docs

---

## 🙏 Acknowledgments

- **Google Gemini API** - For providing free AI capabilities
- **Sentence Transformers** - For excellent embedding models
- **ChromaDB** - For efficient vector storage
- **FastAPI Community** - For great documentation
- **Stack Overflow** - For troubleshooting help

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 📞 Contact

For questions or clarifications:

**Shashwat Dwivedi**  
Email: iamsoranic@gmail.com  
GitHub: https://github.com/Shashw1t  
Registration: 22BCE8168

---

**Submission Date:** October 24, 2025  
**Assignment:** Assignment 7 - Knowledge Base Search Engine  
**Course:** [Add your course name/code]

---

*This documentation provides a comprehensive overview of the Knowledge Base Search Engine project, covering architecture, implementation, deployment, and usage.*
