# AI Resume Analyzer & ATS Optimizer

A production‑grade SaaS that lets users upload a resume, optionally a job description, and receive AI‑powered ATS compatibility scores, keyword gaps, rewritten bullet points, and recruiter‑friendly suggestions.

---

## Table of Contents
- [Tech Stack](#tech-stack)
- [Quick Start (Docker Compose)](#quick-start-docker-compose)
- [Backend API](#backend-api)
- [Frontend UI](#frontend-ui)
- [Database Migrations](#database-migrations)
- [Running Locally without Docker](#running-locally)
- [Environment Variables](#environment-variables)
- [Security Checklist](#security-checklist)
- [Testing](#testing)
- [Deploying to Production](#deploying-to-production)
- [Monetisation Ideas](#monetisation-ideas)

---

## Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Shadcn UI, Framer Motion |
| Backend | FastAPI (Python 3.11), PostgreSQL, SQLAlchemy (async), JWT auth |
| AI | Claude API **or** OpenAI API – abstracted behind `utils/ai_client.py` |
| Containerisation | Docker (multi‑stage) |
| CI / CD | GitHub Actions (lint, test, build) |
| Deployment | Vercel (frontend) + Render/Railway (backend) |

---

## Quick Start (Docker Compose)
```bash
# Clone the repo and cd into it
git clone <repo‑url>
cd ai-resume-optimizer

# Copy example env files and edit the secrets
cp backend/.env.example backend/.env
# edit backend/.env – set DATABASE_URL, JWT_SECRET_KEY, AI keys, etc.

# Build and start containers
docker compose up --build -d

# Apply DB migrations
docker compose exec backend alembic upgrade head

# API docs: http://localhost:8000/docs
# Frontend dev: http://localhost:3000
```

---

## Backend API
All endpoints are versioned under `/api/v1/` and documented in the OpenAPI UI (`/docs`). Key groups:
- **/auth** – signup, login, refresh, logout (JWT stored in HttpOnly cookies)
- **/resumes** – upload/list/delete PDF resumes
- **/analyses** – trigger AI analysis, fetch results
- **/jobs** – store job descriptions and simple keyword‑match endpoint

Authentication is required for every route except `/auth/*`.

---

## Frontend UI
The Next.js app provides:
- Landing page (`/`)
- Auth pages (`/login`, `/signup`, `/reset`)
- Dashboard (`/dashboard`) with tabs for resume upload, analysis history, and JD matching.

The UI uses Shadcn components, Tailwind for styling, and Framer Motion for subtle animations. All API calls go through `src/lib/api.ts` which automatically includes the HttpOnly cookies.

---

## Database Migrations
Alembic is used for schema versioning.
```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "my change"
# Apply migrations
alembic upgrade head
```
The initial migration is `alembic/versions/20240508_initial.py`.

---

## Running Locally (no Docker)
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd ../frontend
npm ci
npm run dev
```
Make sure the `.env` files are present for both sides.

---

## Environment Variables
See `backend/.env.example` and `frontend/.env.local.example` for the full list. Important ones:
- `DATABASE_URL` – PostgreSQL DSN
- `JWT_SECRET_KEY` – 32+ characters
- `CLAUDE_API_KEY` **or** `OPENAI_API_KEY`
- `SMTP_*` – required for email verification (optional placeholder in code)

---

## Security Checklist
- HttpOnly + Secure cookies for JWTs
- BCrypt password hashing (`BCRYPT_ROUNDS`)
- Rate limiting (100 req/min per IP)
- CORS set to `*` in dev, restrict to your domains in prod
- PDF MIME validation + size limit (5 MiB)
- All DB access via SQLAlchemy ORM → no raw SQL → injection safe
- Structured JSON logging via `structlog`
- Secrets never checked into source – loaded from `.env`
- Optional CSRF double‑submit token can be added to state‑changing endpoints

---

## Testing
Backend uses `pytest` with `pytest-asyncio` for async routes. Frontend uses Jest + React Testing Library.
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd ../frontend
npm run test
```
A CI workflow (`.github/workflows/ci.yml`) runs lint, type‑check, tests, and builds Docker images on every PR.

---

## Deploying to Production
1. **Frontend** – push to Vercel (connect repo, set `NEXT_PUBLIC_BACKEND_URL` env var pointing to your backend endpoint). Vercel automatically builds the Docker‑less Next.js app.
2. **Backend** – create a Render/Railway service using the `backend/Dockerfile`. Set environment variables in the service dashboard. Enable automatic migrations (`alembic upgrade head` as a post‑deploy hook).
3. **Database** – use a managed PostgreSQL instance (Supabase, Railway, RDS). Ensure `sslmode=require` in the DSN for production.
4. **TLS** – both services must run behind HTTPS. Render/Railway provide free TLS certificates.
5. **Monitoring** – ship `structlog` JSON logs to a log platform (Datadog, Logtail). Add health‑check endpoint (`/health`) if needed.

---

## Monetisation Ideas
- **Free tier** – 1 analysis per day, limited storage.
- **Pro tier** – unlimited analyses, PDF export, bulk JD matching, priority AI queue.
- **Team tier** – shared workspace, admin console, usage analytics.
- Integrate Stripe for recurring subscriptions; store `stripe_customer_id` in the `subscriptions` table.
- Offer a **white‑label** version for HR agencies (custom branding via a `brand` field on the `User` model).

---

*Ready to ship. Ask me for any missing piece – e.g., email verification implementation, Stripe webhook, additional UI components, or test suites.*
