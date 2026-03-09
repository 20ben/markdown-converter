import anthropic
from anthropic.types import TextBlock

# llm_service.py
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = "claude-haiku-4-5"

_client = None

def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client

prompts = {"short": "Summarize the following markdown content in 2-3 sentences.", 
           "detailed": "Summarize the following markdown content by covering: the main topic, 3-5 key bullet points, and a brief conclusion."}

def summarize(markdown: str, type: str) -> str:

    message = get_client().messages.create(
    model=LLM_MODEL,
    max_tokens=1000,
    messages=[
            {
                "role": "user",
                "content": f"{prompts[type]}\n\n{markdown}",
            }
        ],
    )
    
    block = message.content[0]
    if isinstance(block, TextBlock):
        return block.text
    return ""