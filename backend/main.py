"""
CareerOS Backend — Milestone 1 + Repo List
Entry point: wires up FastAPI app, CORS, and all routers.

Run locally:
    uvicorn main:app --reload --port 8000

Deploy:
    - Railway / Render: use this file directly (uvicorn main:app --host 0.0.0.0 --port $PORT)
    - Vercel: see vercel.json in this same folder
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.analyze import router as analyze_router
from api.github import router as github_router

app = FastAPI(
    title="CareerOS Backend",
    description="GitHub repository/profile analysis backend.",
    version="0.2.0",
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
app.include_router(github_router)


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "service": "careeros-backend"}


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}