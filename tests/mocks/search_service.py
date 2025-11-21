from typing import Dict, Any, List, Optional
from app.services.search_interface import SearchService

class MockSearchService:
    """Mock implementation of SearchService for testing."""
    
    def __init__(self):
        self.mock_responses = {}
    
    def add_response(self, query_snippet: str, response: Dict[str, Any]):
        """Add a mock response for queries containing the snippet."""
        self.mock_responses[query_snippet] = response

    def search(
        self,
        query: str,
        location: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        for snippet, response in self.mock_responses.items():
            if snippet in query:
                return response
        return {"answer": "", "citations": [], "query": query}

    def search_india(
        self,
        query: str,
        region: Optional[str] = None,
        city: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.search(query)

    def search_multiple_queries(
        self, queries: List[str], location: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return [self.search(q) for q in queries]

