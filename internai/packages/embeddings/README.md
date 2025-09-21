# Embeddings Package

This package provides abstractions for embedding generation and similarity search.

## Features

- `EmbeddingsClient`: Abstract interface for embedding operations
- Support for multiple embedding providers
- Vector similarity search capabilities

## Usage

```python
from embeddings import EmbeddingsClient

client = EmbeddingsClient()
embeddings = client.generate_embeddings(["text to embed"])
```
