"""
Predefined Questions for Candidate Data

These questions are based on the Candidate Model fields and allow users
to quickly explore candidate information from the vector database.
"""

from typing import Any, Dict, List

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
