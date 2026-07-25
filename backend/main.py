"""
CareerOS Backend — Milestone 1
Entry point: wires up FastAPI app, CORS, and the /api/analyze router.

Run locally:
    uvicorn main:app --reload --port 8000

Deploy:
    - Railway / Render: use this file directly (uvicorn main:app --host 0.0.0.0 --port $PORT)
    - Vercel: handled via /api/index.py which imports `app` from here (see vercel.json)
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.analyze import router as analyze_router

app = FastAPI(
    title="CareerOS Backend",
    description="Milestone 1: GitHub repository URL -> structured repository JSON.",
    version="0.1.0",
)

_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allow_origins = ["*"] if _origins_env.strip() == "*" else [
    o.strip() for o in _origins_env.split(",") if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "service": "careeros-backend", "milestone": 1}


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}