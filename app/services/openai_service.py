"""
OpenAI Service - Alternative to Perplexity

This service provides search capabilities using OpenAI's API.
More cost-effective for structured data extraction tasks.
"""

import os
from typing import Any, Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from app.services.llm_service import LLMService


class OpenAIService(LLMService):
    """Service for interacting with OpenAI API"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI service.

        Args:
            api_key: OpenAI API key. If not provided, reads from OPENAI_API_KEY env var
            model: Model to use (default: gpt-3.5-turbo for cost efficiency)
        """
        if OpenAI is None:
            raise ImportError(
                "openai package not installed. Install with: pip install openai"
            )

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY "
                "environment variable or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def search(
        self,
        query: str,
        location: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Search using OpenAI API.

        Note: OpenAI doesn't have built-in web search like Perplexity,
        but we can use it for structured data extraction tasks.

        Args:
            query: Search query string
            location: Optional location dict (used to enhance query context)

        Returns:
            Dict containing 'query', 'answer', 'citations', 'model', and 'location'
        """
        # Enhance query with location context if provided
        enhanced_query = query
        if location:
            location_str = location.get("country", "")
            if location.get("region"):
                location_str += f", {location['region']}"
            if location.get("city"):
                location_str += f", {location['city']}"
            if location_str:
                enhanced_query = f"{query} (Context: {location_str})"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides accurate information about Indian politics and elections. "
                        "When providing information, focus on facts and cite sources when possible.",
                    },
                    {"role": "user", "content": enhanced_query},
                ],
                temperature=0.3,  # Lower temperature for more factual responses
            )

            response_content = completion.choices[0].message.content

            return {
                "query": query,
                "answer": response_content,
                "citations": [],  # OpenAI doesn't provide citations like Perplexity
                "model": completion.model,
                "location": location or {},
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
        region: Optional[str] = None,
        city: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convenience method for India-specific searches.

        Args:
            query: Search query string
            region: Indian state/region
            city: Indian city

        Returns:
            Dict containing search results
        """
        location = {"country": "IN"}

        if region:
            location["region"] = region

        if city:
            location["city"] = city

        return self.search(query, location=location)

    def batch_search(
        self,
        queries: List[str],
        location: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search multiple queries. For OpenAI, we can combine them into a single call
        to save costs.

        Args:
            queries: List of search query strings
            location: Optional location filter

        Returns:
            List of result dicts, one per query
        """
        if len(queries) == 1:
            return [self.search(queries[0], location=location)]

        # Combine multiple queries into a single structured request
        combined_query = (
            "I need information about the following topics. "
            "Please provide answers in a structured format:\n\n"
        )
        for i, query in enumerate(queries, 1):
            combined_query += f"{i}. {query}\n"

        combined_query += (
            "\nPlease provide detailed answers for each topic, "
            "separated clearly. Focus on factual information."
        )

        try:
            result = self.search(combined_query, location=location)
            if result.get("error"):
                # Fallback to individual queries
                return [self.search(q, location=location) for q in queries]

            # Parse the combined response (simplified - may need refinement)
            # For now, return the combined result for all queries
            # In production, you might want to parse it into separate responses
            return [result] * len(queries)

        except Exception as e:
            # Fallback to individual queries on error
            return [self.search(q, location=location) for q in queries]

