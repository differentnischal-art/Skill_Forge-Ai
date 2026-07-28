"""
SQLAlchemy ORM models.
Matches the table design in System_design.md §7.
"""

from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

from databases.connection import Base


class User(Base):
    """A logged-in user, created/updated on each GitHub OAuth login."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    career_goal = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_login_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CareerAnalysis(Base):
    """One saved result of POST /api/career-analysis."""

    __tablename__ = "career_analyses"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    career_goal = Column(String, nullable=False)
    strengths = Column(JSON, nullable=False, default=list)
    weaknesses = Column(JSON, nullable=False, default=list)
    missing_skills = Column(JSON, nullable=False, default=list)
    career_readiness = Column(String, nullable=False)
    overall_summary = Column(Text, nullable=False)
    repos_analyzed = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class RepoFeedback(Base):
    """One saved result of POST /api/github/feedback."""

    __tablename__ = "repo_feedback"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String, index=True, nullable=False)
    repo_full_name = Column(String, nullable=False)
    repo_purpose = Column(Text, nullable=False)
    code_quality_estimate = Column(Text, nullable=False)
    documentation_quality = Column(Text, nullable=False)
    suggested_improvements = Column(JSON, nullable=False, default=list)
    missing_evidence_notes = Column(JSON, nullable=False, default=list)
    files_reviewed = Column(JSON, nullable=False, default=list)
    total_source_files_found = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))