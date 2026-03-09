"""
app.py

Flask application entry point.

Exposes two API endpoints:
  POST /api/convert   — converts Markdown to HTML using markdown-it-py
  POST /api/summarize — generates an AI summary via Anthropic Claude
"""


from flask import Flask, Response, request, jsonify
from flask.typing import ResponseReturnValue
from flask_cors import CORS
import os

# For conversion
from markdown_it import MarkdownIt

# For summarization
import ldclient
from ldclient import Context
from ldclient.config import Config
from services.llm_service import summarize

# markdown-it renderer
md = MarkdownIt()

# LaunchDarkly
ldclient.set_config(Config(os.getenv("LAUNCHDARKLY_SDK_KEY", "")))
ld = ldclient.get()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route('/api/convert', methods=['POST'])
def convert() -> Response:
    """
    Convert Markdown to HTML.

    Request body (JSON):
        markdown (str): Raw Markdown text to convert.

    Returns:
        JSON: { "html": str } — the rendered HTML string.
    """

    data = request.get_json()
    markdown = data.get('markdown', '')
    html = md.render(markdown)
    return jsonify({ 'html': html })

@app.route('/api/summarize', methods=['POST'])
def summarize_route() -> ResponseReturnValue:
    """
    Generate an AI summary of the provided Markdown content.

    Request body (JSON):
        markdown (str): Raw Markdown text to summarise.
        user_id  (str): UUID from the client's localStorage.
                        Defaults to "anonymous" if omitted.

    Returns:
        JSON 200: { "summary": str, "variant": str }
            summary — the generated summary text
            variant — the variant assigned to this user
        JSON 403: { "error": "ai_summary_disabled" }
            Returned when the ai-summary-enabled flag is off.
        JSON 502: { "error": str }
            Returned when the Anthropic API call fails.
    """

    data = request.get_json()
    raw = data.get('markdown', '')
    user_id = data.get('user_id', 'anonymous')

    ctx = Context.builder(user_id).kind('user').anonymous(True).build()

    # Although summarize button is hidden anyway, 
    # this disallows user from using API credits by calling this directly
    if not ld.variation('ai-summary-enabled', ctx, False):
        return jsonify({'error': 'ai_summary_disabled'}), 403

    variant = ld.variation('ai-summary-variant', ctx, 'short')

    try:
        result = summarize(raw, variant)
        return jsonify({'summary': result, 'variant': variant})
    except Exception as e:
        return jsonify({'error': str(e)}), 502

if __name__ == '__main__':
    app.run(debug=True, port=5000)
