"""
Perplexity AI Search Service

This service provides search capabilities using the Perplexity AI API,
specifically configured for India-based searches.
"""

import os
from typing import Any, Dict, List, Optional

from perplexityai import Perplexity


class PerplexityService:
    """Service for interacting with Perplexity AI API for search"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Perplexity service.

        Args:
            api_key: Perplexity API key. If not provided, will try to read from
                    PERPLEXITY_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Perplexity API key not provided. Set PERPLEXITY_API_KEY "
                "environment variable or pass api_key parameter."
            )

        # Initialize Perplexity client
        os.environ["PERPLEXITY_API_KEY"] = self.api_key
        self.client = Perplexity()

    def search(
        self,
        query: str,
        max_results: int = 5,
        location: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Search using Perplexity API with India location filter.

        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 5, max: 20)
            location: Custom location dict with keys like 'country', 'region', 'city'.
                     If not provided, defaults to India.

        Returns:
            Dict containing search results with 'query', 'results', and metadata

        Example:
            >>> service = PerplexityService()
            >>> results = service.search("election results Delhi 2025")
            >>> for result in results['results']:
            ...     print(result['title'], result['url'])
        """
        # Default to India if no location specified
        if location is None:
            location = {"country": "IN"}

        try:
            # Use chat completions API with web search enabled
            # This is the primary method for Perplexity searches
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": query}],
                model="sonar",  # sonar model is optimized for search
                web_search_options={"user_location": location},
            )

            # Extract response
            response_content = completion.choices[0].message.content
            citations = getattr(completion, "citations", [])

            return {
                "query": query,
                "answer": response_content,
                "citations": citations,
                "model": completion.model,
                "location": location,
            }

        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "answer": None,
                "citations": [],
            }

    def search_india(
        self,
        query: str,
        max_results: int = 5,
        region: Optional[str] = None,
        city: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convenience method for India-specific searches.

        Args:
            query: Search query string
            max_results: Maximum number of results
            region: Indian state/region (e.g., "Delhi", "Maharashtra", "Karnataka")
            city: Indian city (e.g., "New Delhi", "Mumbai", "Bengaluru")

        Returns:
            Dict containing search results

        Example:
            >>> service = PerplexityService()
            >>> results = service.search_india(
            ...     "best political news",
            ...     region="Delhi",
            ...     city="New Delhi"
            ... )
        """
        location = {"country": "IN"}

        if region:
            location["region"] = region

        if city:
            location["city"] = city

        return self.search(query, max_results=max_results, location=location)

    def search_multiple_queries(
        self, queries: List[str], location: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search multiple queries in batch.

        Args:
            queries: List of search query strings
            location: Location filter (defaults to India)

        Returns:
            List of result dicts, one per query
        """
        results = []
        for query in queries:
            result = self.search(query, location=location)
            results.append(result)

        return results
