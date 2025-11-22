import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class VectorDBService:
    """
    Service for interacting with ChromaDB to store and retrieve vector embeddings.
    Designed to be fast and simple, using a local persistent directory.
    """

    def __init__(self, collection_name: str = "candidates", persist_path: str = "data/chroma_db"):
        """
        Initialize the VectorDBService.

        Args:
            collection_name: Name of the collection to use.
            persist_path: Path to the local directory for storing the database.
        """
        self.persist_path = persist_path
        self.collection_name = collection_name
        
        # Ensure directory exists
        os.makedirs(persist_path, exist_ok=True)

        try:
            self.client = chromadb.PersistentClient(path=persist_path)
            self.collection = self.client.get_or_create_collection(name=collection_name)
            logger.info(f"VectorDBService initialized with collection '{collection_name}' at '{persist_path}'")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None, ids: Optional[List[str]] = None):
        """
        Add texts to the vector database.

        Args:
            texts: List of text strings to add.
            metadatas: List of metadata dictionaries corresponding to texts.
            ids: List of unique IDs. If None, auto-generated.
        """
        try:
            if ids is None:
                # Generate simple IDs if not provided
                import uuid
                ids = [str(uuid.uuid4()) for _ in texts]
            
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(texts)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding texts to ChromaDB: {e}")
            raise

    def query_similar(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query for similar texts.

        Args:
            query_text: The query string.
            n_results: Number of top results to return.

        Returns:
            List of dictionaries containing 'document', 'metadata', and 'distance'.
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            # Parse results into a cleaner format
            parsed_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    parsed_results.append({
                        "id": results['ids'][0][i],
                        "document": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else None
                    })
            
            return parsed_results
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}")
            return []

    def get_top_questions(self, n: int = 5) -> List[str]:
        """
        Retrieve the top N questions stored (assuming questions are stored as documents).
        This is a placeholder logic; usually 'top' implies some metric. 
        For now, it returns the first N items or most recent if we add timestamps.
        """
        # efficiently peek at the data
        try:
            result = self.collection.peek(limit=n)
            return result['documents'] if result['documents'] else []
        except Exception as e:
            logger.error(f"Error peeking ChromaDB: {e}")
            return []

