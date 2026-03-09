from flask import Flask, request, jsonify
from flask_cors import CORS

# for conversion
from markdown_it import MarkdownIt
md = MarkdownIt()

# for summarization
import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from services.llm_service import summarize

# LaunchDarkly
ldclient.set_config(Config(os.getenv("LAUNCHDARKLY_SDK_KEY", "")))
ld = ldclient.get()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    markdown = data.get('markdown', '')
    html = md.render(markdown)
    return jsonify({ 'html': html })

@app.route('/api/summarize', methods=['POST'])
def summarize_route():

    data = request.get_json()
    raw = data.get('markdown', '')
    user_id = data.get('user_id', 'anonymous')

    ctx = Context.builder(user_id).kind('user').anonymous(True).build()

    # although summarize button is hidden anyway, 
    #   this disallows user from using API credits by calling this directly
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
