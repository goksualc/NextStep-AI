import numpy as np
from mistralai import Mistral


class EmbeddingsClient:
    def __init__(self, api_key: str, model: str = "mistral-embed"):
        self.client = Mistral(api_key=api_key)
        self.model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # Batch call; the SDK exposes an embeddings endpoint per docs.
        resp = self.client.embeddings.create(model=self.model, inputs=texts)
        # Unify to plain list of floats
        return [e.embedding for e in resp.data]


# Also add a cosine_similarity helper:
def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-12
    return float(np.dot(a, b) / denom)
