import os
import json
from openai import OpenAI

from llm.defin_tools import TOOLS
from tools.banker_recommendation_tool import banker_recommendation_tool

# Ensure your OpenAI API key is set in the environment variables, or replace with your key directly.
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI

messages = [
    {
        "role": "user",
        "content": "Generate a banking recommendation for Maria Lopez."  # John Smith
    }
]

response = client.chat.completions.create(
    model="openai:gpt-5.1",
    messages=messages,
    tools=TOOLS
)

msg = response.choices[0].message
print("MODEL MESSAGE:", msg)

if msg.tool_calls:
    tool_call = msg.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    tool_response = banker_recommendation_tool(**args)
    print("TOOL RESPONSE:", tool_response)
