from typing import List, Dict, Any, Optional
from config import settings
try:
    import openai
except ImportError:
    openai = None
try:
    import anthropic
except ImportError:
    anthropic = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None


class LLMService:
    """Handles LLM integration for answer synthesis."""
    
    def __init__(self):
        self.provider = settings.llm_provider.lower()
        self.model = settings.llm_model
        
        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            openai.api_key = settings.openai_api_key
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            if anthropic is None:
                raise ValueError("Anthropic package not installed")
            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        elif self.provider == "google":
            if not settings.google_api_key:
                raise ValueError("Google API key not configured")
            if genai is None:
                raise ValueError("Google Generative AI package not installed")
            genai.configure(api_key=settings.google_api_key)
            self.client = genai.GenerativeModel(self.model)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def synthesize_answer(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """Generate an answer using retrieved context."""
        try:
            # Build context from retrieved chunks
            context = self._build_context(context_chunks)
            
            # Create prompt
            prompt = self._create_prompt(query, context)
            
            # Generate answer based on provider
            if self.provider == "openai":
                answer = self._generate_openai(prompt, max_tokens)
            elif self.provider == "anthropic":
                answer = self._generate_anthropic(prompt, max_tokens)
            elif self.provider == "google":
                answer = self._generate_google(prompt, max_tokens)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            return {
                "success": True,
                "answer": answer,
                "query": query,
                "num_sources": len(context_chunks),
                "model": self.model
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": None
            }
    
    def _build_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved chunks."""
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            text = chunk.get('text', '')
            metadata = chunk.get('metadata', {})
            filename = metadata.get('filename', 'Unknown')
            
            context_parts.append(f"[Source {i} - {filename}]\n{text}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create the prompt for the LLM."""
        prompt = f"""You are a helpful assistant that answers questions based on provided documents.

Using the following documents, answer the user's question succinctly and accurately.

IMPORTANT INSTRUCTIONS:
- Base your answer ONLY on the information provided in the documents below
- If the documents don't contain enough information to answer the question, say so
- Cite which sources you used when possible
- Be concise but comprehensive
- If you're unsure, acknowledge the uncertainty

DOCUMENTS:
{context}

QUESTION: {query}

ANSWER:"""
        return prompt
    
    def _generate_openai(self, prompt: str, max_tokens: int) -> str:
        """Generate response using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided documents."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    
    def _generate_anthropic(self, prompt: str, max_tokens: int) -> str:
        """Generate response using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.content[0].text.strip()
    
    def _generate_google(self, prompt: str, max_tokens: int) -> str:
        """Generate response using Google Gemini API."""
        try:
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": max_tokens,
            }
            print(f"[DEBUG] Calling Gemini API with model: {self.model}")
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config
            )
            print(f"[DEBUG] Gemini response received")
            return response.text.strip()
        except Exception as e:
            print(f"[ERROR] Gemini API call failed: {str(e)}")
            print(f"[ERROR] Error type: {type(e).__name__}")
            raise
    
    def test_connection(self) -> Dict[str, Any]:
        """Test LLM connection."""
        try:
            test_prompt = "Say 'Hello' if you can receive this message."
            
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": test_prompt}],
                    max_tokens=10
                )
                return {
                    "success": True,
                    "provider": self.provider,
                    "model": self.model,
                    "message": "Connection successful"
                }
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=10,
                    messages=[{"role": "user", "content": test_prompt}]
                )
                return {
                    "success": True,
                    "provider": self.provider,
                    "model": self.model,
                    "message": "Connection successful"
                }
            elif self.provider == "google":
                response = self.client.generate_content(test_prompt)
                return {
                    "success": True,
                    "provider": self.provider,
                    "model": self.model,
                    "message": "Connection successful"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
