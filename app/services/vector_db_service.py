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

    def __init__(self, collection_name: str = "candidates", persist_path: str = None):
        """
        Initialize the VectorDBService.

        Args:
            collection_name: Name of the collection to use.
            persist_path: Path to the local directory for storing the database.
                         If None, uses the default path from environment or 'data/chroma_db'.
        """
        # Use environment variable or default path
        if persist_path is None:
            persist_path = os.getenv("CHROMA_DB_PATH", "data/chroma_db")

        self.persist_path = persist_path
        self.collection_name = collection_name

        # Ensure directory exists
        os.makedirs(persist_path, exist_ok=True)

        try:
            self.client = chromadb.PersistentClient(path=persist_path)
            self.collection = self.client.get_or_create_collection(name=collection_name)
            logger.info(
                f"VectorDBService initialized with collection '{collection_name}' at '{persist_path}'"
            )
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ):
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

            self.collection.add(documents=texts, metadatas=metadatas, ids=ids)
            logger.info(f"Added {len(texts)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding texts to ChromaDB: {e}")
            raise

    def query_similar(
        self, query_text: str, n_results: int = 5
    ) -> List[Dict[str, Any]]:
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
                query_texts=[query_text], n_results=n_results
            )

            # Parse results into a cleaner format
            parsed_results = []
            if results["documents"]:
                for i in range(len(results["documents"][0])):
                    parsed_results.append(
                        {
                            "id": results["ids"][0][i],
                            "document": results["documents"][0][i],
                            "metadata": results["metadatas"][0][i]
                            if results["metadatas"]
                            else {},
                            "distance": results["distances"][0][i]
                            if results["distances"]
                            else None,
                        }
                    )

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
            return result["documents"] if result["documents"] else []
        except Exception as e:
            logger.error(f"Error peeking ChromaDB: {e}")
            return []

    def upsert_candidate_data(
        self, candidate_id: str, text: str, metadata: Dict[str, Any]
    ):
        """
        Insert or update candidate data in the vector database.

        Args:
            candidate_id: Unique identifier for the candidate
            text: Text representation of candidate data for embedding
            metadata: Metadata about the candidate (name, party, constituency, etc.)
        """
        try:
            self.collection.upsert(
                documents=[text], metadatas=[metadata], ids=[candidate_id]
            )
            logger.info(f"Upserted candidate {candidate_id} to ChromaDB")
        except Exception as e:
            logger.error(f"Error upserting candidate {candidate_id} to ChromaDB: {e}")
            raise

    def delete_candidate(self, candidate_id: str):
        """
        Delete a candidate from the vector database.

        Args:
            candidate_id: Unique identifier for the candidate
        """
        try:
            self.collection.delete(ids=[candidate_id])
            logger.info(f"Deleted candidate {candidate_id} from ChromaDB")
        except Exception as e:
            logger.error(f"Error deleting candidate {candidate_id} from ChromaDB: {e}")
            raise

    def get_candidate(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a candidate by ID.

        Args:
            candidate_id: Unique identifier for the candidate

        Returns:
            Dictionary with candidate document and metadata, or None if not found
        """
        try:
            result = self.collection.get(ids=[candidate_id])
            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "document": result["documents"][0] if result["documents"] else None,
                    "metadata": result["metadatas"][0] if result["metadatas"] else {},
                }
            return None
        except Exception as e:
            logger.error(f"Error getting candidate {candidate_id} from ChromaDB: {e}")
            return None

    def count_candidates(self) -> int:
        """
        Get the total number of candidates in the collection.

        Returns:
            Number of candidates in the collection
        """
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error counting candidates in ChromaDB: {e}")
            return 0
