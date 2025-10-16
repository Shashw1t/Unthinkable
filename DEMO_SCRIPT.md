# Demo Script for Knowledge Base Search Engine

This script provides a step-by-step guide for demonstrating the Knowledge Base Search Engine in a video presentation.

## Pre-Demo Setup (Do this before recording)

1. ✅ Ensure all dependencies are installed
2. ✅ Configure API key in `.env`
3. ✅ Clear any previous data: `curl -X DELETE http://localhost:8000/clear`
4. ✅ Prepare sample documents (in `sample_documents/` folder)
5. ✅ Test the application is working
6. ✅ Close unnecessary browser tabs and applications
7. ✅ Set screen recording to 1920x1080
8. ✅ Have script notes ready

## Demo Script (5-7 minutes)

### Scene 1: Introduction (30 seconds)
**[Show: GitHub repository or project folder]**

"Hello! Today I'm demonstrating a Knowledge Base Search Engine that uses RAG - Retrieval-Augmented Generation - to answer questions from your documents using AI.

This project features:
- Document upload and processing for PDF, TXT, and DOCX files
- Intelligent text chunking and embedding generation
- Vector database storage with ChromaDB
- Semantic similarity search
- AI-powered answer synthesis using OpenAI GPT
- Clean web interface"

### Scene 2: Architecture Overview (45 seconds)
**[Show: README.md architecture diagram or code structure]**

"The architecture consists of several components:

1. Document Processor - handles text extraction from various formats
2. RAG Engine - generates embeddings and performs semantic search using Sentence Transformers
3. Vector Database - ChromaDB stores and retrieves document chunks efficiently
4. LLM Service - integrates with OpenAI to synthesize answers
5. FastAPI Backend - provides RESTful endpoints
6. Frontend - simple, modern web interface

The data flow is straightforward: documents are uploaded, processed into chunks, embedded, and stored. When you query, we retrieve relevant chunks and use an LLM to synthesize a natural answer."

### Scene 3: Starting the Application (30 seconds)
**[Show: Terminal/Command Prompt]**

"Let's start the application. I'll run the startup script which handles everything automatically."

```powershell
# Run in terminal
.\start.bat
# or
python setup_and_run.py
```

**[Wait for server to start, show startup messages]**

"The server is now running on localhost:8000. Let me open it in the browser."

### Scene 4: Web Interface Tour (30 seconds)
**[Show: Browser at http://localhost:8000]**

"Here's the web interface. We have:
- Upload section on the left where you can drag and drop documents
- Query section on the right for asking questions
- Statistics dashboard at the bottom showing indexed documents and chunks"

### Scene 5: Uploading Documents (1.5 minutes)
**[Show: Upload process]**

"Let me upload a couple of sample documents. I have documents about machine learning and Python programming."

**Actions:**
1. Drag `machine_learning_intro.txt` to upload area
2. Drag `python_guide.txt` to upload area
3. Click "Upload Documents"
4. **[Wait for processing]**

"As you can see, the documents are being processed. The system:
1. Extracts text from the files
2. Cleans and normalizes the content
3. Splits text into overlapping chunks for better context preservation
4. Generates embeddings using Sentence Transformers
5. Stores them in the ChromaDB vector database

The machine learning document was processed into 15 chunks, and the Python guide into 12 chunks. Notice the statistics updated showing 27 total chunks indexed."

### Scene 6: Querying - Example 1 (1 minute)
**[Show: Query interface]**

"Now let's ask some questions. First, let me ask about machine learning."

**Type:** "What is machine learning and what are its main types?"

**Click Search**

"The system is now:
1. Converting my query into an embedding
2. Searching the vector database for similar chunks
3. Retrieving the top 5 most relevant pieces of context
4. Sending them to GPT along with my question
5. GPT synthesizes a natural answer based only on the retrieved context

And here's the answer! As you can see, it correctly explains machine learning and identifies the three main types: supervised, unsupervised, and reinforcement learning. 

Below the answer, we can see the source documents it used - showing transparency and allowing users to verify the information."

### Scene 7: Querying - Example 2 (45 seconds)
**[Show: Query interface]**

**Type:** "What are the popular Python libraries for data science?"

**Click Search**

"Here's another question about Python libraries. The answer correctly identifies NumPy, Pandas, Matplotlib, Scikit-learn, TensorFlow, and PyTorch - all from the Python guide document we uploaded.

Notice how the system only uses information from our documents, not its general knowledge. This is the power of RAG - grounding AI responses in your specific data."

### Scene 8: Querying - Example 3 (30 seconds)
**[Show: Query interface]**

**Type:** "How does reinforcement learning work?"

**Click Search**

"One more example - asking about reinforcement learning specifically. The answer explains that an agent learns through trial and error to maximize reward, and even provides examples like AlphaGo and robotics, all extracted from our uploaded documents."

### Scene 9: API Demonstration (1 minute)
**[Show: Browser at http://localhost:8000/docs]**

"The project also includes a full REST API. FastAPI provides automatic interactive documentation at the /docs endpoint.

Here we can see all available endpoints:
- POST /upload for document ingestion
- POST /query for asking questions
- GET /stats for knowledge base statistics
- DELETE /clear to reset the database

Let me try a quick API call."

**[Show: Terminal or Swagger UI]**

```powershell
# Example API call
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "What is Python used for?"}'
```

**[Show response]**

"And we get a JSON response with the answer, sources, and metadata. This API can be integrated into other applications, chatbots, or automated workflows."

### Scene 10: Code Walkthrough (1 minute)
**[Show: VS Code or code editor]**

"Let me quickly show the code structure. Opening the project in VS Code:

**[Show `document_processor.py`]**
- Document Processor handles text extraction from PDFs, DOCX, and TXT files
- Includes text cleaning and intelligent chunking with overlap

**[Show `rag_engine.py`]**
- RAG Engine manages the vector database
- Uses Sentence Transformers for embeddings
- Implements semantic similarity search with ChromaDB

**[Show `llm_service.py`]**
- LLM Service integrates with OpenAI or Anthropic
- Handles prompt engineering
- Synthesizes answers from retrieved context

**[Show `main.py`]**
- FastAPI application with all endpoints
- CORS enabled for frontend integration
- Comprehensive error handling

The code is well-structured, modular, and follows best practices with type hints and documentation."

### Scene 11: Evaluation Criteria (30 seconds)
**[Show: README.md or presentation slide]**

"This project addresses all evaluation criteria:

✅ **Retrieval Accuracy**: Semantic search with configurable similarity thresholds and intelligent chunking

✅ **Synthesis Quality**: Integration with state-of-the-art LLMs, careful prompt engineering, and source citations

✅ **Code Structure**: Clean separation of concerns, modular architecture, comprehensive error handling

✅ **LLM Integration**: Support for multiple providers, flexible configuration, efficient token usage"

### Scene 12: Conclusion (30 seconds)
**[Show: GitHub repository or application]**

"To summarize, this Knowledge Base Search Engine provides:
- Easy document upload and processing
- Powerful RAG-based retrieval
- AI-generated answers with source citations
- Clean API and web interface
- Production-ready code structure

The complete code, documentation, and setup instructions are available in the GitHub repository. Thank you for watching!"

## Post-Demo Checklist

✅ Export video in HD (1920x1080)
✅ Add video title and description
✅ Upload to YouTube
✅ Add video link to README.md
✅ Create GitHub repository
✅ Push all code to GitHub
✅ Test repository clone and setup process
✅ Add video link to repository description

## Recording Tips

1. **Audio Quality**: Use a good microphone, eliminate background noise
2. **Pace**: Speak clearly and at a moderate pace
3. **Screen**: Use 1920x1080 resolution, hide personal information
4. **Editing**: 
   - Speed up waiting times (document processing, API responses)
   - Add captions for key points
   - Use zoom/highlight for code sections
5. **Professional**: Be enthusiastic but professional

## Backup Demo Questions

If time permits, try these additional questions:
- "What are the challenges in machine learning?"
- "What makes Python easy to learn?"
- "Name some applications of machine learning in healthcare"
- "What is the difference between supervised and unsupervised learning?"

## Common Issues During Demo

**Issue**: Upload takes too long
- **Solution**: Use smaller sample documents or pre-process them

**Issue**: API response is slow
- **Solution**: Use GPT-3.5-turbo instead of GPT-4 for faster responses

**Issue**: No relevant results found
- **Solution**: Ensure query is related to uploaded documents

## Video Editing Checklist

✅ Remove dead air and long pauses
✅ Add intro slide (project name + your name)
✅ Add outro slide (GitHub link + thank you)
✅ Add background music (optional, keep it subtle)
✅ Add captions/subtitles for important points
✅ Ensure audio levels are consistent
✅ Export in MP4 format, H.264 codec
✅ Final video should be 5-7 minutes

Good luck with your demo! 🎥
