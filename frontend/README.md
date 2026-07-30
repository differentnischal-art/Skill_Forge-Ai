# SkillForge Frontend

## Setup

    cd frontend
    npm install
    npm run dev

Opens at http://localhost:3000. Backend must be running on :8000 simultaneously.

## Auth flow
1. Landing page button → backend /api/auth/github/login
2. GitHub → backend /api/auth/github/callback
3. Backend redirects to http://localhost:3000/auth/callback?token=...
4. Frontend stores token, redirects to /dashboard
5. Dashboard calls /api/auth/me, then /api/github/repos/{username}

## Known simplifications
- Token in localStorage (fine for local dev, revisit before public deploy)
- No server-side auth guard yet — client-side redirect only