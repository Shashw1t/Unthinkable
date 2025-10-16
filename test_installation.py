"""
Test script to verify the Knowledge Base Search Engine installation
"""
import sys
import importlib


def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'chromadb': 'ChromaDB',
        'sentence_transformers': 'Sentence Transformers',
        'openai': 'OpenAI',
        'PyPDF2': 'PyPDF2',
        'fitz': 'PyMuPDF',
        'docx': 'python-docx',
        'pydantic': 'Pydantic',
    }
    
    failed = []
    
    for package, name in packages.items():
        try:
            importlib.import_module(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            failed.append(name)
    
    return len(failed) == 0, failed


def test_modules():
    """Test if custom modules can be imported."""
    print("\nTesting custom modules...")
    
    modules = [
        'config',
        'document_processor',
        'rag_engine',
        'llm_service',
        'main'
    ]
    
    failed = []
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}.py")
        except Exception as e:
            print(f"✗ {module}.py - ERROR: {str(e)[:50]}")
            failed.append(module)
    
    return len(failed) == 0, failed


def test_env_file():
    """Check if .env file exists."""
    print("\nChecking configuration...")
    
    import os
    
    if os.path.exists('.env'):
        print("✓ .env file exists")
        
        # Check if API key is set
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if openai_key and openai_key != 'your_openai_api_key_here':
            print("✓ OpenAI API key is configured")
        elif anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
            print("✓ Anthropic API key is configured")
        else:
            print("⚠ No API key configured (required for LLM features)")
            return False
        
        return True
    else:
        print("✗ .env file not found")
        print("  Run setup_and_run.py to create it")
        return False


def test_directories():
    """Check if required directories exist or can be created."""
    print("\nChecking directories...")
    
    import os
    
    dirs = ['uploaded_documents', 'chroma_db', 'frontend']
    
    for directory in dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}/ exists")
        else:
            print(f"⚠ {directory}/ not found (will be created on first run)")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Knowledge Base Search Engine - Installation Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test imports
    success, failed = test_imports()
    results.append(('Package Imports', success, failed))
    
    # Test modules
    success, failed = test_modules()
    results.append(('Custom Modules', success, failed))
    
    # Test env file
    success = test_env_file()
    results.append(('Configuration', success, []))
    
    # Test directories
    success = test_directories()
    results.append(('Directories', success, []))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed, failed_items in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if failed_items:
            print(f"  Failed: {', '.join(failed_items)}")
        all_passed = all_passed and passed
    
    print()
    
    if all_passed:
        print("🎉 All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("1. Configure your API key in .env file")
        print("2. Run: python setup_and_run.py")
        print("3. Open: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: copy .env.example .env")
        print("3. Configure API keys in .env")
    
    print("\n" + "=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
