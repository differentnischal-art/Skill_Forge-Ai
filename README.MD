# 🚀 SkillForge AI

> **Stop asking "How many commits have I made?"**
>
> **Start asking "What should I build next?"**

SkillForge AI is an AI-powered developer feedback platform that analyzes GitHub repositories and provides actionable, evidence-based insights about a developer's strengths, weaknesses, and skill gaps.

Instead of relying on GitHub contribution graphs or repository counts, SkillForge evaluates the actual quality of your work and helps you understand what to improve to become industry-ready.

---

## 🌐 Live Demo

**Application:** https://skill-forge-ai-five.vercel.app

---

## ✨ Features

- 🔐 Secure GitHub OAuth Login
- 👤 GitHub Profile Integration
- 📂 Repository Analysis
- 🤖 AI-Powered Code Feedback
- 📈 Developer Strength Assessment
- 🎯 Skill Gap Identification
- 🛠 Personalized Improvement Suggestions
- ⚡ Fast Full-Stack Architecture
- 🔒 JWT Authentication

---

## 🛠 Tech Stack

### Frontend

- Next.js 16
- React
- TypeScript
- Tailwind CSS

### Backend

- FastAPI
- SQLAlchemy
- Python
- JWT Authentication

### AI

- Google Gemini API

### Database

- SQLite (Development)
- Easily configurable for PostgreSQL

### Deployment

- Vercel

---

# Project Structure

```
Skill_Forge-Ai/

├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── ...
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── databases/
│   ├── schemas/
│   └── ...
│
└── README.md
```

---

# Architecture

```
User

   │

   ▼

Next.js Frontend

   │

GitHub OAuth Login

   │

   ▼

FastAPI Backend

   │

GitHub REST API

   │

Repository Data

   │

Gemini AI Analysis

   │

JWT Session

   │

   ▼

Developer Dashboard
```

---

# Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/differentnischal-art/Skill_Forge-Ai.git

cd Skill_Forge-Ai
```

---

# Backend Setup

## Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
cd backend

pip install -r requirements.txt
```

---

## Create Environment File

Create

```
backend/.env
```

Example

```env
APP_ENV=local

GITHUB_CLIENT_ID=YOUR_CLIENT_ID
GITHUB_CLIENT_SECRET=YOUR_CLIENT_SECRET

GITHUB_OAUTH_REDIRECT_URI=http://localhost:8000/api/auth/github/callback

FRONTEND_URL=http://localhost:3000

JWT_SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_api_key

ALLOWED_ORIGINS=http://localhost:3000
```

---

## Run Backend

```bash
uvicorn main:app --reload --port 8000
```

Backend runs at

```
http://localhost:8000
```

---

# Frontend Setup

Open another terminal.

```bash
cd frontend

npm install
```

Create

```
frontend/.env.local
```

Example

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Run

```bash
npm run dev
```

Frontend runs at

```
http://localhost:3000
```

---

# GitHub OAuth Configuration

Create a GitHub OAuth App.

Set:

Homepage URL

```
http://localhost:3000
```

Authorization Callback URL

```
http://localhost:8000/api/auth/github/callback
```

For production:

Homepage

```
https://skill-forge-ai-five.vercel.app
```

Callback

```
https://skill-forge-ai-five.vercel.app/api/auth/github/callback
```

---

# Environment Variables

Backend

| Variable | Required |
|-----------|----------|
| GITHUB_CLIENT_ID | ✅ |
| GITHUB_CLIENT_SECRET | ✅ |
| JWT_SECRET_KEY | ✅ |
| GEMINI_API_KEY | ✅ |
| FRONTEND_URL | ✅ |
| GITHUB_OAUTH_REDIRECT_URI | ✅ |
| ALLOWED_ORIGINS | ✅ |

Frontend

| Variable | Required |
|-----------|----------|
| NEXT_PUBLIC_API_BASE_URL | ✅ |

---

# API Endpoints

Authentication

```
GET /api/auth/github/login

GET /api/auth/github/callback

GET /api/auth/me
```

Repository Analysis

```
POST /api/analyze

GET /api/github/repos
```

Health Check

```
GET /health
```

---

# Requirements

## Software

- Python 3.11+
- Node.js 20+
- npm
- Git

---

## Accounts

- GitHub Account
- GitHub OAuth App
- Google Gemini API Key
- Vercel Account (for deployment)

---

# Deployment

The application is deployed on **Vercel**.

Production URL

```
https://skill-forge-ai-five.vercel.app
```

Deploy your own:

```bash
git clone ...

Create environment variables

Connect GitHub repository

Deploy using Vercel
```

---

# Current Status

✅ GitHub OAuth Authentication

✅ JWT Authentication

✅ GitHub Profile Fetching

✅ Repository Analysis

✅ AI Feedback Generation

🚧 Advanced Analytics

🚧 Recruiter Dashboard

🚧 Multi-user Workspace

---

# Roadmap

- Repository Comparison
- Historical Progress Tracking
- AI Learning Roadmap
- Recruiter Dashboard
- Resume Intelligence
- Portfolio Scoring
- Team Analytics
- Skill Progress Timeline

---

# Contributing

Contributions are welcome.

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit

```bash
git commit -m "Add feature"
```

4. Push

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

# License

This project is licensed under the MIT License.

---

# Authors

**Nischal Adhikari**

AI & Data Science Student

GitHub:
https://github.com/differentnischal-art

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and supports future development.