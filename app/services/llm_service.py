"""
Abstract LLM Service Interface

This module provides a unified interface for different LLM providers,
allowing easy switching between Perplexity, OpenAI, Anthropic, etc.
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    PERPLEXITY = "perplexity"
    OPENAI = "openai"


class LLMService(ABC):
    """Abstract base class for LLM services"""

    @abstractmethod
    def search(
        self,
        query: str,
        location: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Search using LLM with optional location filter.

        Args:
            query: Search query string
            location: Optional location dict with keys like 'country', 'region', 'city'

        Returns:
            Dict containing 'query', 'answer', 'citations', 'model', and 'location'
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def batch_search(
        self,
        queries: List[str],
        location: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search multiple queries efficiently (may combine into single call).

        Args:
            queries: List of search query strings
            location: Optional location filter

        Returns:
            List of result dicts, one per query
        """
        pass


def get_llm_service(
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
) -> LLMService:
    """
    Factory function to get the appropriate LLM service.

    Args:
        provider: Provider name ('perplexity', 'openai', 'anthropic').
                 If None, reads from LLM_PROVIDER env var or defaults to 'perplexity'
        api_key: Optional API key. If not provided, reads from provider-specific env var

    Returns:
        LLMService instance

    Example:
        >>> service = get_llm_service('openai')
        >>> results = service.search("election results")
    """
    # Determine provider
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "perplexity").lower()

    provider_enum = LLMProvider(provider)

    # Import and instantiate the appropriate service
    if provider_enum == LLMProvider.PERPLEXITY:
        from app.services.perplexity_service import PerplexityService

        if api_key is None:
            api_key = os.getenv("PERPLEXITY_API_KEY")
        return PerplexityService(api_key=api_key)

    elif provider_enum == LLMProvider.OPENAI:
        from app.services.openai_service import OpenAIService

        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        return OpenAIService(api_key=api_key)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

