
from bank_recommendation.llm.rag_pipeline import format_similar_customers


def build_prompt(customer, similar_customers):
    """Build a prompt for the LLM based on customer and similar customer data."""
    formatted_patterns = format_similar_customers(similar_customers)

    return f"""
You are a banking advisor.

Customer Profile:
Name: {customer['name']}
Age: {customer['age']}
Balance: ${customer['balance']}
Account Type: {customer['account_type']}
Occupation: {customer['occupation']}

Similar Customer Patterns:
{formatted_patterns}

Task:
Recommend the best financial action for this customer.

Rules:
- Return ONLY the recommendation (1–2 sentences).
- Do NOT include JSON, lists, or explanations.
- Do NOT repeat any input data.
"""
