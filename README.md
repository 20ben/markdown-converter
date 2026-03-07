# Markdown Converter

A web app that converts Markdown to HTML in real-time, with an AI summarization feature gated behind LaunchDarkly feature flags and an A/B experiment comparing summary styles.

**Stack:** Python + Flask · React + Vite + TypeScript · Anthropic Claude API · LaunchDarkly

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/)
- A [LaunchDarkly](https://launchdarkly.com/) account with the flags set up (see below)

---

## LaunchDarkly Setup

Before running the app, create the following in your LD project:

---

## Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)

# Install dependencies
pip install -r requirements.txt
```

Populate `backend/.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
LAUNCHDARKLY_SDK_KEY=sdk-...
```

Start the server:

```bash
python app.py
# Running on http://localhost:5000
```

---

## Frontend Setup

Populate `frontend/.env`:

```
VITE_API_BASE_URL=http://localhost:5000/api
VITE_LAUNCHDARKLY_CLIENT_ID=your-client-side-id-here
```

Install dependencies and start the dev server:

```bash
cd frontend
npm install
npm run dev
# Running on http://localhost:5173
```
---