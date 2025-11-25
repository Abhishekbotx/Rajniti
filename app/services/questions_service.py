"""
Questions Service

This service manages predefined questions and retrieves answers
from the ChromaDB vector database for candidate-related queries.
"""

import logging
from typing import Any, Dict, List, Optional

from app.services.vector_db_service import VectorDBService

logger = logging.getLogger(__name__)


# Top 5 predefined questions based on the Candidate Model
PREDEFINED_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "q1",
        "question": "What is the educational background of this candidate?",
        "category": "education",
        "description": "Get details about the candidate's education, colleges, and qualifications.",
    },
    {
        "id": "q2",
        "question": "What is the political history of this candidate?",
        "category": "political",
        "description": "View past elections contested, party affiliations, and results.",
    },
    {
        "id": "q3",
        "question": "What are the declared assets of this candidate?",
        "category": "assets",
        "description": "See the financial assets declared by the candidate.",
    },
    {
        "id": "q4",
        "question": "Are there any criminal cases against this candidate?",
        "category": "crime",
        "description": "Check if the candidate has any pending or resolved criminal cases.",
    },
    {
        "id": "q5",
        "question": "What is the family background of this candidate?",
        "category": "family",
        "description": "Learn about the candidate's family members and their professions.",
    },
]


class QuestionsService:
    """
    Service for managing predefined questions and fetching answers
    from the vector database.
    """

    def __init__(self, vector_db_service: Optional[VectorDBService] = None):
        """
        Initialize the QuestionsService.

        Args:
            vector_db_service: Optional VectorDBService instance.
                             If not provided, a new instance will be created.
        """
        self.vector_db = vector_db_service or VectorDBService(
            collection_name="candidates"
        )
        logger.info("QuestionsService initialized successfully")

    def get_predefined_questions(self) -> List[Dict[str, Any]]:
        """
        Get the list of top 5 predefined questions.

        Returns:
            List of predefined question dictionaries.
        """
        return PREDEFINED_QUESTIONS.copy()

    def answer_question(
        self,
        question: str,
        candidate_id: Optional[str] = None,
        n_results: int = 5,
    ) -> Dict[str, Any]:
        """
        Answer a question using semantic search on the vector database.

        Args:
            question: The question to answer.
            candidate_id: Optional candidate ID to filter results.
            n_results: Number of similar documents to retrieve.

        Returns:
            Dictionary with answer, related candidates, and metadata.
        """
        try:
            logger.info(f"Answering question: {question[:50]}...")

            # Query the vector database
            results = self.vector_db.query_similar(question, n_results=n_results)

            if not results:
                return {
                    "success": True,
                    "question": question,
                    "answer": "No relevant information found in the database.",
                    "candidates": [],
                    "total_results": 0,
                }

            # If candidate_id is provided, filter results
            if candidate_id:
                results = [
                    r
                    for r in results
                    if r.get("metadata", {}).get("candidate_id") == candidate_id
                ]

            # Format the response
            candidates_info = []
            for result in results:
                metadata = result.get("metadata", {})
                candidates_info.append(
                    {
                        "candidate_id": metadata.get("candidate_id", ""),
                        "name": metadata.get("name", "Unknown"),
                        "party_id": metadata.get("party_id", ""),
                        "constituency_id": metadata.get("constituency_id", ""),
                        "state_id": metadata.get("state_id", ""),
                        "status": metadata.get("status", ""),
                        "relevance_score": 1 - result.get("distance", 0)
                        if result.get("distance") is not None
                        else None,
                        "document": result.get("document", ""),
                    }
                )

            # Generate a summary answer from the top results
            answer = self._generate_answer(question, results)

            return {
                "success": True,
                "question": question,
                "answer": answer,
                "candidates": candidates_info,
                "total_results": len(candidates_info),
            }

        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "success": False,
                "question": question,
                "answer": f"Error processing question: {str(e)}",
                "candidates": [],
                "total_results": 0,
            }

    def _generate_answer(
        self, question: str, results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a human-readable answer from search results.

        Args:
            question: The original question.
            results: List of search results from vector DB.

        Returns:
            A formatted answer string.
        """
        if not results:
            return "No relevant information found."

        question_lower = question.lower()

        # Determine the category of question
        if "education" in question_lower:
            return self._format_education_answer(results)
        elif "political" in question_lower or "history" in question_lower:
            return self._format_political_answer(results)
        elif "asset" in question_lower or "wealth" in question_lower:
            return self._format_assets_answer(results)
        elif "criminal" in question_lower or "crime" in question_lower or "case" in question_lower:
            return self._format_crime_answer(results)
        elif "family" in question_lower:
            return self._format_family_answer(results)
        else:
            return self._format_general_answer(results)

    def _format_education_answer(self, results: List[Dict[str, Any]]) -> str:
        """Format answer for education-related questions."""
        answers = []
        for result in results[:3]:  # Top 3 results
            doc = result.get("document", "")
            name = result.get("metadata", {}).get("name", "Unknown")
            if "Education:" in doc:
                edu_part = doc.split("Education:")[1].split(".")[0].strip()
                answers.append(f"{name}: {edu_part}")
        return "; ".join(answers) if answers else "No education information available."

    def _format_political_answer(self, results: List[Dict[str, Any]]) -> str:
        """Format answer for political history questions."""
        answers = []
        for result in results[:3]:
            doc = result.get("document", "")
            name = result.get("metadata", {}).get("name", "Unknown")
            if "Political History:" in doc:
                pol_part = doc.split("Political History:")[1].split(".")[0].strip()
                answers.append(f"{name}: {pol_part}")
            else:
                status = result.get("metadata", {}).get("status", "")
                party = result.get("metadata", {}).get("party_id", "")
                answers.append(f"{name}: {status} with {party}")
        return "; ".join(answers) if answers else "No political history available."

    def _format_assets_answer(self, results: List[Dict[str, Any]]) -> str:
        """Format answer for assets-related questions."""
        answers = []
        for result in results[:3]:
            doc = result.get("document", "")
            name = result.get("metadata", {}).get("name", "Unknown")
            if "Assets:" in doc:
                assets_part = doc.split("Assets:")[1].split(".")[0].strip()
                answers.append(f"{name}: {assets_part}")
        return "; ".join(answers) if answers else "No asset information available."

    def _format_crime_answer(self, results: List[Dict[str, Any]]) -> str:
        """Format answer for criminal case questions."""
        answers = []
        for result in results[:3]:
            doc = result.get("document", "")
            name = result.get("metadata", {}).get("name", "Unknown")
            crime_count = result.get("metadata", {}).get("crime_cases_count", 0)
            if "Criminal Cases:" in doc:
                crime_part = doc.split("Criminal Cases:")[1].split(".")[0].strip()
                answers.append(f"{name}: {crime_part}")
            elif crime_count:
                answers.append(f"{name}: {crime_count} criminal case(s)")
            else:
                answers.append(f"{name}: No criminal cases on record")
        return "; ".join(answers) if answers else "No criminal case information available."

    def _format_family_answer(self, results: List[Dict[str, Any]]) -> str:
        """Format answer for family-related questions."""
        answers = []
        for result in results[:3]:
            doc = result.get("document", "")
            name = result.get("metadata", {}).get("name", "Unknown")
            if "Family:" in doc:
                fam_part = doc.split("Family:")[1].split(".")[0].strip()
                answers.append(f"{name}: {fam_part}")
        return "; ".join(answers) if answers else "No family information available."

    def _format_general_answer(self, results: List[Dict[str, Any]]) -> str:
        """Format a general answer from search results."""
        answers = []
        for result in results[:3]:
            name = result.get("metadata", {}).get("name", "Unknown")
            party = result.get("metadata", {}).get("party_id", "")
            status = result.get("metadata", {}).get("status", "")
            answers.append(f"{name} ({party}) - {status}")
        return "; ".join(answers) if answers else "No relevant information found."

    def answer_predefined_question(
        self,
        question_id: str,
        candidate_id: Optional[str] = None,
        n_results: int = 5,
    ) -> Dict[str, Any]:
        """
        Answer a predefined question by its ID.

        Args:
            question_id: The ID of the predefined question.
            candidate_id: Optional candidate ID to filter results.
            n_results: Number of similar documents to retrieve.

        Returns:
            Dictionary with answer and metadata.
        """
        # Find the question by ID
        question_data = next(
            (q for q in PREDEFINED_QUESTIONS if q["id"] == question_id), None
        )

        if not question_data:
            return {
                "success": False,
                "error": f"Question with ID '{question_id}' not found.",
                "question": None,
                "answer": None,
                "candidates": [],
            }

        # Answer the question
        result = self.answer_question(
            question=question_data["question"],
            candidate_id=candidate_id,
            n_results=n_results,
        )

        # Add question metadata
        result["question_id"] = question_id
        result["category"] = question_data["category"]

        return result
