""" RAG-based Banker Recommendation Tool """

import numpy as np
from bank_recommendation.embeddings.embedder import get_embedding
from bank_recommendation.retrieve.retriever import retrieve_similar
from bank_recommendation.llm.prompt_templates import build_prompt, format_similar_customers
from bank_recommendation.llm.rag_pipeline import generate_rag_response
from bank_recommendation.llm.final_formatting import format_final_response


def rag_banker_recommendation_tool(name: str, customers, index):

    customer = next(
        (c for c in customers if c["name"].lower() == name.lower()), None)

    if not customer:
        return {"error": f"Customer '{name}' not found"}

    query_text = f"{customer['age']} {customer['occupation']} {customer['balance']}"
    query_embedding = np.array(get_embedding(
        query_text)).astype("float32").reshape(1, -1)

    similar_ids = retrieve_similar(index, query_embedding)
    similar_customers = [customers[int(i)] for i in similar_ids[0]]

    formatted_similar = format_similar_customers(similar_customers)

    prompt = build_prompt(customer, formatted_similar)

    llm_result = generate_rag_response(prompt)

    return {
        "message": format_final_response(customer["name"], llm_result)
        # "debug": {
        #     "based_on": formatted_similar
        # }
    }
