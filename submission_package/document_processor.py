import os
import re
from typing import List, Dict, Any
import PyPDF2
try:
    import fitz  # PyMuPDF (optional)
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    print("PyMuPDF not available, using PyPDF2 for PDF processing")
from docx import Document as DocxDocument
from pathlib import Path
from config import settings


class DocumentProcessor:
    """Handles document ingestion and text extraction."""
    
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF if available, otherwise PyPDF2."""
        # Try PyMuPDF first (if available)
        if HAS_PYMUPDF:
            try:
                text = ""
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text()
                doc.close()
                return text.strip()
            except Exception as e:
                print(f"PyMuPDF failed, falling back to PyPDF2: {e}")
        
        # Use PyPDF2 as fallback or primary method
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text.strip()
        except Exception as e2:
            raise Exception(f"Failed to extract PDF text: {str(e2)}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX files."""
        try:
            doc = DocxDocument(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract DOCX text: {str(e)}")
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read().strip()
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from various file formats."""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might cause issues
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split text into overlapping chunks."""
        chunk_size = chunk_size or settings.chunk_size
        overlap = overlap or settings.chunk_overlap
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence or word boundary
            if end < len(text):
                # Look for sentence end
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                last_boundary = max(last_period, last_newline)
                
                if last_boundary > chunk_size * 0.5:  # At least 50% of chunk
                    end = start + last_boundary + 1
                    chunk = text[start:end]
                else:
                    # Look for word boundary
                    last_space = chunk.rfind(' ')
                    if last_space > chunk_size * 0.5:
                        end = start + last_space
                        chunk = text[start:end]
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    def process_document(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Process a document: extract text, clean, and chunk."""
        try:
            # Extract text
            raw_text = self.extract_text(file_path)
            
            # Clean text
            cleaned_text = self.clean_text(raw_text)
            
            # Chunk text
            chunks = self.chunk_text(cleaned_text)
            
            return {
                "filename": filename,
                "file_path": file_path,
                "text": cleaned_text,
                "chunks": chunks,
                "num_chunks": len(chunks),
                "success": True
            }
        except Exception as e:
            return {
                "filename": filename,
                "file_path": file_path,
                "error": str(e),
                "success": False
            }
