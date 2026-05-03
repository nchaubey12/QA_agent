# QA Agent v2

A production-ready Question-Answering agent built with **Google ADK**, **Gemini 2.5 Flash**, and **FastAPI** — served with a built-in HTML dashboard.

---

## Architecture

```
dashboard.html  →  GET /         (serves the UI)
FastAPI (main.py)  →  POST /ask  (receives context + question)
    ↓
Runner (Google ADK)
    ↓
root_agent (agent.py)  →  uses answer_question tool (tools.py)
    ↓
Gemini 2.5 Flash (via Google GenAI)
```

- **`main.py`** — FastAPI app, session management, `/ask` endpoint, dashboard route
- **`agent.py`** — ADK `Agent` definition with model, instructions, and tool binding
- **`tools.py`** — `answer_question` tool: formats context + question into a structured prompt
- **`dashboard.html`** — Frontend UI served directly by FastAPI
- **`Dockerfile`** — Container image based on `python:3.11-slim`, exposes port 8080
- **`Procfile`** — For Heroku / Railway / Cloud Run deployment via uvicorn

---

## Prerequisites

- Python 3.11+
- A **Google Cloud project** with the Gemini API enabled
- `GOOGLE_API_KEY` or Application Default Credentials (ADC) set up

---

## Local Setup

```bash
# 1. Clone / unzip project
cd qa-agent-v2

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key in the terminal session (no .env file needed)
export GOOGLE_API_KEY=your_key_here   # Mac/Linux
set GOOGLE_API_KEY=your_key_here      # Windows CMD
$env:GOOGLE_API_KEY="your_key_here"   # Windows PowerShell

# 5. Run the server
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

> The key is only set for the current terminal session — it disappears when you close it. Nothing is written to disk.

Open `http://localhost:8080` in your browser to use the dashboard.

---

## API Key (No .env Required)

This project reads `GOOGLE_API_KEY` directly from your environment — no `.env` file or extra libraries needed.

Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey) and export it before running the server as shown above.

If you later want to use a `.env` file (e.g. for team setup), add `python-dotenv` to `requirements.txt` and add these two lines at the top of `main.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

A `.env.example` template is included in the repo for reference.

---

## API

### `POST /ask`

**Request body:**
```json
{
  "context": "The Eiffel Tower is located in Paris, France.",
  "question": "Where is the Eiffel Tower?"
}
```

**Response:**
```json
{
  "answer": "The Eiffel Tower is located in Paris, France."
}
```

### `GET /health`
Returns `{"status": "ok"}` — use for uptime checks.

---

## Docker

```bash
docker build -t qa-agent-v2 .
docker run -e GOOGLE_API_KEY=your_key_here -p 8080:8080 qa-agent-v2
```

---

## Deployment

The `Procfile` supports one-click deploy to **Heroku**, **Railway**, or **Google Cloud Run**.

For Cloud Run:
```bash
gcloud run deploy qa-agent-v2 \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=your_key_here \
  --allow-unauthenticated
```

> **Tip:** On Cloud Run, use Secret Manager instead of `--set-env-vars` for the API key.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | Yes | Gemini API key from Google AI Studio |
| `PORT` | No | Server port (default: 8080) |

---

## Dependencies

```
google-adk>=0.5.0
google-genai
fastapi
uvicorn[standard]
pydantic
```