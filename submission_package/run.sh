#!/bin/bash
# Quick Start Script for Knowledge Base Search Engine

echo "============================================================"
echo "  Knowledge Base Search Engine with Google Gemini"
echo "============================================================"
echo ""
echo "Starting server at http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the server"
echo ""

venv/Scripts/python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
