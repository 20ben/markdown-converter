import anthropic
from anthropic.types import TextBlock
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = "claude-haiku-4-5"

# Client starts at none, only gets fully initialized once it's first used.
_client = None

def get_client() -> Anthropic:
    """
    Return the shared Anthropic client, creating it on first call.
    SDK only initialises once for the lifetime of the Flask process.

    Returns:
        Anthropic: The initialized Anthropic API client.
    """

    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client

# Prompt templates keyed by LaunchDarkly variant value.
PROMPTS: dict[str, str] = {"short": "Summarize the following markdown content in 2-3 sentences.", 
           "detailed": "Summarize the following markdown content by covering: the main topic, 3-5 key bullet points, and a brief conclusion."}

def summarize(markdown: str, type: str) -> str:
    """
    Generate a plain-text summary of the given Markdown content. 
    Selects the prompt template based on the LaunchDarkly variant.

    Args:
        markdown: Raw Markdown string to summarize.
        variant:  LaunchDarkly variant key — either "short" or "detailed".

    Returns:
        The summary text returned by Claude, or an empty string if the
        response contained no TextBlock (should not happen).

    Raises:
        anthropic.APIError: If the Anthropic API returns an error
                            (e.g. invalid key, rate limit). The
                            caller in app.py catches this and returns 502.
    """

    message = get_client().messages.create(
    model=LLM_MODEL,
    max_tokens=1000,
    messages=[
            {
                "role": "user",
                "content": f"{PROMPTS[type]}\n\n{markdown}",
            }
        ],
    )
    
    block = message.content[0]
    if isinstance(block, TextBlock):
        return block.text
    return ""