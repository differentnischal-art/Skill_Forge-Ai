# CareerOS Backend — Milestone 1

**Scope:** GitHub repository URL in → structured repository JSON out. No AI yet.

## Run locally

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env .env.local               # fill in GITHUB_TOKEN if you have one
uvicorn main:app --reload --port 8000
```

Test it:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/vercel/next.js"}'
```

Interactive docs: http://localhost:8000/docs

## Deploy

### Option A — Railway / Render (recommended for FastAPI)
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Set env vars `GITHUB_TOKEN` and `ALLOWED_ORIGINS` in the dashboard.
- No extra config files needed.

### Option B — Vercel
- This repo includes `vercel.json`, which builds `main.py` with `@vercel/python`
  and routes all traffic to it, so the ASGI app runs as a serverless function.
- Set `GITHUB_TOKEN` and `ALLOWED_ORIGINS` under Project Settings → Environment Variables.
- Note: cold starts and the 10s default execution limit on Vercel's free tier are
  worth keeping in mind once AI calls (Day 4) are added to this backend — Railway/Render
  are the more predictable choice once LLM latency enters the picture.

## Endpoints

| Method | Path          | Description                          |
|--------|---------------|---------------------------------------|
| GET    | `/`           | Health check                          |
| GET    | `/health`     | Health check                          |
| POST   | `/api/analyze`| `{ "repo_url": "..." }` → repo JSON   |
