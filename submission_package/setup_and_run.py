"""
Knowledge Base Search Engine - Setup and Run Script
"""
import os
import sys


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    if not os.path.exists('.env'):
        print("Creating .env file from template...")
        with open('.env.example', 'r') as template:
            content = template.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✓ .env file created. Please edit it with your API keys.")
        return False
    return True


def check_dependencies():
    """Check if required packages are installed."""
    try:
        import fastapi
        import uvicorn
        import chromadb
        import sentence_transformers
        import openai
        print("✓ All dependencies are installed.")
        return True
    except ImportError as e:
        print(f"✗ Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def create_directories():
    """Create necessary directories."""
    dirs = ['uploaded_documents', 'chroma_db']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("✓ Directories created.")


def main():
    print("=" * 60)
    print("Knowledge Base Search Engine - Setup")
    print("=" * 60)
    
    # Create .env file
    env_exists = create_env_file()
    
    if not env_exists:
        print("\n⚠ Please configure your .env file with API keys before running.")
        print("Edit .env and add your OpenAI or Anthropic API key.")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create directories
    create_directories()
    
    print("\n" + "=" * 60)
    print("Setup Complete! Starting the server...")
    print("=" * 60)
    print("\nAccess the application at: http://localhost:8000")
    print("Press Ctrl+C to stop the server.\n")
    
    # Start the server
    import uvicorn
    from main import app
    from config import settings
    
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
