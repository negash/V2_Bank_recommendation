"""Module for the RAG pipeline that generates responses based on retrieved similar customers."""
import json
from openai import OpenAI

client = OpenAI()


def generate_rag_response(prompt):
    """Generate a response using the RAG pipeline with the given prompt."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a banking recommendation engine.\n"
                    "Return ONLY valid JSON.\n"
                    "No explanations, no markdown, no extra text.\n\n"

                    "Schema:\n"
                    "{\n"
                    "  \"recommendations\": [\n"
                    "    {\n"
                    "      \"action\": \"string\",\n"
                    "      \"reason\": \"string\",\n"
                    "      \"risk_level\": \"low|medium|high\",\n"
                    "      \"confidence\": number\n"
                    "    }\n"
                    "  ]\n"
                    "}\n\n"

                    "Rules:\n"
                    "- confidence must be between 0 and 1\n"
                    "- use higher confidence when similar customers show consistent behavior\n"
                    "- Return exactly 2–3 distinct recommendations"
                    "- Each recommendation must be meaningfully different (not reworded)"
                )
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=200  # Set the maximum number of tokens in the generated response
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "action": "Invalid model output",
            "reason": content,
            "risk_level": "unknown",
            "confidence": 0.0
        }


def format_similar_customers(similar_customers):
    """Format the list of similar customers into a readable string."""
    patterns = []

    for c in similar_customers:

        if isinstance(c, dict):
            occupation = c.get("occupation", "Unknown")
            age = c.get("age", "Unknown")
            balance = c.get("balance", 0)
            account_type = c.get("account_type", "").lower()
        else:
            occupation = getattr(c, "occupation", "Unknown")
            age = getattr(c, "age", "Unknown")
            balance = getattr(c, "balance", 0)
            account_type = getattr(c, "account_type", "").lower()

        action = (
            "kept funds in savings and earned interest"
            if account_type == "saving"
            else "moved funds to higher-yield accounts"
        )

        patterns.append(
            f"- {occupation}, age {age}, balance ${balance:,}: {action}"
        )

    return "\n".join(patterns)
