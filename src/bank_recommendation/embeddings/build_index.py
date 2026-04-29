import faiss
import numpy as np


def build_faiss_index(embeddings):
    """NumPy converts the embeddings into a contiguous float32 matrix, which FAISS can efficiently index and search."""
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]  # safer than len()
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index
