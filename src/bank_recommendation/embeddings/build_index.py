import faiss
import numpy as np


def build_faiss_index(embeddings):
    """Build a FAISS index from a list of embeddings."""
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]  # safer than len()
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index
