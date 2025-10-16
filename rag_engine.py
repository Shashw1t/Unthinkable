import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import uuid
from config import settings


class RAGEngine:
    """Handles embeddings generation, vector storage, and retrieval."""
    
    def __init__(self):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=settings.chroma_db_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def add_documents(self, chunks: List[str], metadata: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add document chunks to the vector database."""
        try:
            print(f"[DEBUG] Adding {len(chunks)} chunks to collection")
            print(f"[DEBUG] First chunk preview: {chunks[0][:100]}...")
            
            # Generate unique IDs for each chunk
            ids = [str(uuid.uuid4()) for _ in chunks]
            
            # Generate embeddings
            embeddings = self.generate_embeddings(chunks)
            print(f"[DEBUG] Generated {len(embeddings)} embeddings")
            
            # Add to ChromaDB
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadata
            )
            
            # Verify addition
            count = self.collection.count()
            print(f"[DEBUG] Collection now has {count} total documents")
            
            return {
                "success": True,
                "num_chunks_added": len(chunks),
                "chunk_ids": ids
            }
        except Exception as e:
            print(f"[ERROR] Failed to add documents: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def search(self, query: str, top_k: int = None) -> Dict[str, Any]:
        """Search for relevant documents using semantic similarity."""
        top_k = top_k or settings.top_k_results
        
        try:
            # Check if collection has any documents
            count = self.collection.count()
            print(f"[DEBUG] Collection has {count} documents")
            
            if count == 0:
                return {
                    "success": True,
                    "query": query,
                    "results": [],
                    "num_results": 0,
                    "debug": "No documents in collection"
                }
            
            # Generate query embedding
            query_embedding = self.generate_embeddings([query])[0]
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, count)
            )
            
            # Format results
            documents = results.get('documents', [[]])[0]
            metadatas = results.get('metadatas', [[]])[0]
            distances = results.get('distances', [[]])[0]
            
            print(f"[DEBUG] Found {len(documents)} raw results")
            print(f"[DEBUG] Distances: {distances}")
            
            # Convert distances to similarity scores (1 - distance for cosine)
            similarities = [1 - dist for dist in distances]
            print(f"[DEBUG] Similarities: {similarities}")
            print(f"[DEBUG] Threshold: {settings.similarity_threshold}")
            
            # Filter by similarity threshold
            filtered_results = []
            for doc, meta, sim in zip(documents, metadatas, similarities):
                if sim >= settings.similarity_threshold:
                    filtered_results.append({
                        "text": doc,
                        "metadata": meta,
                        "similarity": sim
                    })
            
            print(f"[DEBUG] Filtered to {len(filtered_results)} results")
            
            return {
                "success": True,
                "query": query,
                "results": filtered_results,
                "num_results": len(filtered_results)
            }
        except Exception as e:
            print(f"[ERROR] Search failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        try:
            count = self.collection.count()
            return {
                "success": True,
                "total_chunks": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def clear_collection(self) -> Dict[str, Any]:
        """Clear all documents from the collection."""
        try:
            self.chroma_client.delete_collection("knowledge_base")
            self.collection = self.chroma_client.create_collection(
                name="knowledge_base",
                metadata={"hnsw:space": "cosine"}
            )
            return {
                "success": True,
                "message": "Collection cleared successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
