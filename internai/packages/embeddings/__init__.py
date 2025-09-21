"""
Embeddings package for InternAI

Provides abstractions for text embeddings using various providers.
"""

from .client import EmbeddingsClient

__version__ = "1.0.0"
__all__ = ["EmbeddingsClient"]
