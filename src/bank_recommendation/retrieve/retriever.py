
def retrieve_similar(index, query_embedding, k=5):
    """Module for retrieving similar customers based on query embeddings."""
    distances, indices = index.search(query_embedding, k)
    return indices
