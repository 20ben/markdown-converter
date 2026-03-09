# Marconv

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

Before running the app, create the following in your LaunchDarkly project under the **Test** environment (or whichever environment you choose).

### 1. Feature Flags

| Flag key | Type | Purpose |
|---|---|---|
| `ai-summary-enabled` | Boolean | Gates the entire AI summary feature. When off, the Summary panel is hidden and the backend returns `403`. |
| `ai-summary-variant` | String (multivariate) | Controls which prompt is used. Variations: `short`, `detailed`. |

**`ai-summary-variant` variations to create:**
- `short` — value: `short`
- `detailed` — value: `detailed`

### 2. Experiment & Metric

1. In **Metrics**, create a new metric:
   - **Name:** Helpful Click
   - **Event key:** `helpful-click`
   - **Event kind:** Custom
   - **Success criteria:** Higher is better

2. In **Experiments**, create a new experiment linked to the `ai-summary-variant` flag:
   - Add the **Helpful Click** metric
   - Set the traffic allocation (e.g. 50% / 50%)

### 3. SDK Keys

You'll need two keys from the LaunchDarkly dashboard (**Account settings → Projects → your project → Test environment**):

| Key | Where used |
|---|---|
| **SDK key** (`sdk-...`) | `backend/.env` — used by the Python server SDK |
| **Client-side ID** (`65abc...`) | `frontend/.env` — used by the React client SDK |

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