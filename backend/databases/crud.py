"""
Database read/write functions.
Kept separate from the API layer per ADR-006 (modular monolith) —
routes call these functions, never touch the DB session directly.
"""

from sqlalchemy.orm import Session

from databases.model import CareerAnalysis, RepoFeedback


def save_career_analysis(
    db: Session,
    username: str,
    career_goal: str,
    strengths: list[str],
    weaknesses: list[str],
    missing_skills: list[str],
    career_readiness: str,
    overall_summary: str,
    repos_analyzed: int,
) -> CareerAnalysis:
    record = CareerAnalysis(
        username=username,
        career_goal=career_goal,
        strengths=strengths,
        weaknesses=weaknesses,
        missing_skills=missing_skills,
        career_readiness=career_readiness,
        overall_summary=overall_summary,
        repos_analyzed=repos_analyzed,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_career_analyses_for_user(db: Session, username: str) -> list[CareerAnalysis]:
    return (
        db.query(CareerAnalysis)
        .filter(CareerAnalysis.username == username)
        .order_by(CareerAnalysis.created_at.desc())
        .all()
    )


def save_repo_feedback(
    db: Session,
    repo_url: str,
    repo_full_name: str,
    repo_purpose: str,
    code_quality_estimate: str,
    documentation_quality: str,
    suggested_improvements: list[str],
    missing_evidence_notes: list[str],
    files_reviewed: list[str],
    total_source_files_found: int,
) -> RepoFeedback:
    record = RepoFeedback(
        repo_url=repo_url,
        repo_full_name=repo_full_name,
        repo_purpose=repo_purpose,
        code_quality_estimate=code_quality_estimate,
        documentation_quality=documentation_quality,
        suggested_improvements=suggested_improvements,
        missing_evidence_notes=missing_evidence_notes,
        files_reviewed=files_reviewed,
        total_source_files_found=total_source_files_found,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_feedback_history_for_repo(db: Session, repo_url: str) -> list[RepoFeedback]:
    return (
        db.query(RepoFeedback)
        .filter(RepoFeedback.repo_url == repo_url)
        .order_by(RepoFeedback.created_at.desc())
        .all()
    )