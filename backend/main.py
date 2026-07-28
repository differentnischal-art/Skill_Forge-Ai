"""
SkillForge Backend
Entry point: wires up FastAPI app, CORS, database tables, and all routers.

Run locally:
    uvicorn main:app --reload --port 8000
"""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.analyze import router as analyze_router
from api.auth import router as auth_router
from api.github import router as github_router
from databases.connection import Base, engine
from databases import model

app = FastAPI(
    title="SkillForge Backend",
    description="GitHub repository/profile analysis backend.",
    version="0.4.0",
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


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(analyze_router)
app.include_router(auth_router)
app.include_router(github_router)


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "service": "skillforge-backend"}


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}