# Quick Start Guide

## Installation Steps (Windows)

1. **Double-click `start.bat`** - This will:
   - Create a virtual environment
   - Install all dependencies
   - Start the server automatically

2. **Configure your API key**:
   - Open the `.env` file created in the project folder
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-key-here
     ```
   - Save the file

3. **Restart the application** by running `start.bat` again

4. **Open your browser** to http://localhost:8000

## Installation Steps (Mac/Linux)

1. **Run the startup script**:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

2. **Configure your API key**:
   - Edit the `.env` file:
     ```bash
     nano .env
     ```
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-key-here
     ```
   - Save (Ctrl+O, Enter, Ctrl+X)

3. **Restart** by running `./start.sh` again

4. **Open your browser** to http://localhost:8000

## Getting an OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Click on "API Keys" in the left sidebar
4. Click "Create new secret key"
5. Copy the key and paste it into your `.env` file

**Note**: You'll need billing set up on your OpenAI account. The API usage will be charged based on OpenAI's pricing.

## Alternative: Using Free Embedding Models

If you want to test the system without LLM costs, you can:

1. Upload and index documents (works without API key)
2. Use the `/stats` endpoint to verify documents are indexed
3. The retrieval system works independently

For full functionality with answer generation, an LLM API key is required.

## Testing the Installation

1. **Upload a test document**:
   - Use the sample documents in `sample_documents/` folder
   - Drag and drop onto the upload area
   - Wait for "Successfully processed" message

2. **Ask a test question**:
   - Type: "What is machine learning?"
   - Click "Search"
   - You should see an AI-generated answer with sources

## Troubleshooting

**Issue**: Dependencies won't install
- **Solution**: Make sure you have Python 3.8+ installed
- Check: `python --version`

**Issue**: Port 8000 already in use
- **Solution**: Edit `.env` and change `PORT=8000` to `PORT=8001`

**Issue**: API key error
- **Solution**: Verify your OpenAI API key is correct in `.env`
- Make sure there are no extra spaces or quotes

**Issue**: Documents not uploading
- **Solution**: Check file size (max 10MB by default)
- Verify file format (PDF, TXT, or DOCX only)

## Project Structure

```
Unthinkable1/
├── frontend/           # Web interface
├── sample_documents/   # Example documents
├── main.py            # FastAPI application
├── config.py          # Configuration
├── document_processor.py  # Document handling
├── rag_engine.py      # RAG implementation
├── llm_service.py     # LLM integration
└── README.md          # Full documentation
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the API at http://localhost:8000/docs
3. Try uploading your own documents
4. Experiment with different queries

## Support

If you encounter issues:
1. Check the troubleshooting section in README.md
2. Verify all dependencies are installed
3. Ensure your API key is configured correctly
4. Check the terminal for error messages

Happy searching! 🔍
