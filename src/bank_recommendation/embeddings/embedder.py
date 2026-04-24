"""Module for generating text embeddings using OpenAI's API."""
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
""" Please provide your OpenAI API key as an environment variable. or paste it here OPENAI_API_KEY = "your_api_key_here" """


def get_embedding(text: str):
    """Get embedding for a given text using OpenAI's API."""
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding
