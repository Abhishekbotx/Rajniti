from typing import Protocol, Dict, Any, Optional, List

class SearchService(Protocol):
    def search(
        self,
        query: str,
        location: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        ...

    def search_india(
        self,
        query: str,
        region: Optional[str] = None,
        city: Optional[str] = None,
    ) -> Dict[str, Any]:
        ...

    def search_multiple_queries(
        self, queries: List[str], location: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        ...

