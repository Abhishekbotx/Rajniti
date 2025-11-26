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
        "question": "How many candidates have criminal cases?",
        "category": "criminal",
        "description": "Get details about the candidate's criminal cases.",
    },
    {
        "id": "q2",
        "question": "How many candidates have bachelor's degree?",
        "category": "education",
        "description": "Get details about the candidate's education background.",
    },
    {
        "id": "q3",
        "question": "How many candidates have 1Crore or more assets?",
        "category": "assets",
        "description": "Get details about the candidate's assets.",
    },
]
