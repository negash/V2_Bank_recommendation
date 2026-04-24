"""API module for bank product recommendations using FastAPI."""
from fastapi import FastAPI
from pydantic import BaseModel
import re

from src.bank_recommendation.embeddings.embedder import get_embedding
from src.bank_recommendation.embeddings.build_index import build_faiss_index
from src.bank_recommendation.tools.rag_banker_tool import rag_banker_recommendation_tool
from src.bank_recommendation.data.Customers_data import get_customers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bank Recommendation API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Request(BaseModel):
    """Request model for recommendation API."""
    name: str


class ChatRequest(BaseModel):
    """Request model for chat API."""
    message: str


# Initialize once at startup
customers = get_customers()
embeddings = [get_embedding(str(c)) for c in customers]
index = build_faiss_index(embeddings)


@app.post("/recommend")
def recommend(req: Request):
    """API endpoint to get product recommendations for a customer."""
    result = rag_banker_recommendation_tool(
        name=req.name,
        customers=customers,
        index=index
    )
    return result


@app.post("/chat")
def chat(req: ChatRequest):
    user_message = req.message.strip()

    name = extract_name(user_message)

    if not name:
        return {
            "response": "Please provide a customer name (e.g., 'Recommend for John')."
        }

    result = rag_banker_recommendation_tool(
        name=name,
        customers=customers,
        index=index
    )

    return {"response": format_response(result)}

# ------------------------
# Helper functions
# ------------------------


def extract_name(text: str) -> str:
    """
    Try to extract a name from user input.
    """

    # Pattern: "for John" or "for John Doe"
    match = re.search(r"for ([A-Za-z ]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Fallback: single word input
    words = text.split()
    if len(words) == 1:
        return words[0]

    return None


def format_response(result) -> str:
    """ Convert RAG output into chat-friendly text  """

    if isinstance(result, dict):
        lines = []
        for key, value in result.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)

    return str(result)
