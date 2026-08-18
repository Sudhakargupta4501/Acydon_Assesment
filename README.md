# JobFlow — Production-Quality Job Data Ingestion System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg?style=flat&logo=React&logoColor=black)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC.svg?style=flat&logo=Tailwind-CSS&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A production-ready full-stack job data ingestion engine and monitoring dashboard built for the **Acdyon Technologies Frontend Challenge — Part 1: "Getting Data Out of a Platform That Doesn't Want You To."**

---

## 🌟 Key Features

- **Permitted Public Data Sources:** Ingests live job listings from permitted public RSS feeds (e.g. WeWorkRemotely RSS), REST APIs (Arbeitnow), and sandbox mock feeds. Zero TOS violations, no stealth scrapers, no CAPTCHA bypassing.
- **Resilient ETL Ingestion Pipeline:** 6-stage lifecycle (`Fetch` → `Parse` → `Normalize` → `Validate` → `Deduplicate` → `Store`).
- **Responsible Request Pacing & Retry:** Integrated `SafeHttpClient` with configurable timeouts, minimum request interval pacing (2s default), and exponential backoff retry.
- **Dual-Layer Deduplication:** Primary key checks on `source + external_id` and SHA-256 fingerprint hash matching on `title + company + location + source_url`.
- **Schema Validation & Error Auditing:** Pydantic schema enforcement; invalid records are caught and recorded to `ingestion_errors` without halting execution.
- **Automated Background Scheduler:** Integrated `APScheduler` executing background job collection every 60 minutes.
- **Modern Developer Dashboard:** Glassmorphism UI with real-time statistics, instant search with debouncing, multi-filter queries, paginated job lists, detailed views, and live pipeline status monitoring.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph Data Sources
        RSS[Public Job RSS Feed]
        API[Public REST API]
        MOCK[Sandbox Mock Source]
    end

    subgraph Backend Pipeline (FastAPI & SQLAlchemy)
        Adapter[JobSource Adapter Interface]
        Client[Safe HTTP Client & Exponential Backoff]
        Norm[Data Normalizer]
        Val[Pydantic Schema Validator]
        Dedupe[SHA-256 Fingerprint Deduplicator]
        Store[(Database - SQLite / PostgreSQL)]
        Sched[APScheduler Background Job]
    end

    subgraph Frontend Dashboard (React + Vite + Tailwind)
        Dash[Metrics & Job Search Dashboard]
        IngestUI[Live Pipeline Status & Trigger]
    end

    RSS --> Adapter
    API --> Adapter
    MOCK --> Adapter
    Adapter --> Client
    Client --> Norm
    Norm --> Val
    Val -->|Valid| Dedupe
    Val -->|Malformed| Store
    Dedupe -->|Unique| Store
    Sched --> Adapter
    Store <--> FastAPI REST Endpoints
    FastAPI REST Endpoints <--> Dash
    FastAPI REST Endpoints <--> IngestUI
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons, Axios |
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy, Pydantic v2, APScheduler |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Testing** | Pytest, Pytest-Asyncio, HTTPX TestClient |

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Clone Repository
```bash
git clone https://github.com/acdyon/job-data-ingestion.git
cd job-data-ingestion
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment settings
cp .env.example .env

# Run FastAPI Dev Server
uvicorn app.main:app --reload --port 8000
```
Backend API will be live at: `http://localhost:8000` (Swagger UI documentation at `http://localhost:8000/docs`).

### 3. Frontend Setup
In a new terminal window:
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite Dev Server
npm run dev
```
Frontend Dashboard will be live at: `http://localhost:5173`.

---

## 🧪 Running Tests

To run the backend test suite (unit tests for normalizer, validator, deduplicator, pipeline, and API endpoints):

```bash
# Set PYTHONPATH to include backend directory
$env:PYTHONPATH="backend"  # PowerShell
# export PYTHONPATH=backend  # Bash / Linux

backend/venv/Scripts/python -m pytest backend/tests -v
```

---

## 🌐 API Reference Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/jobs` | Search & filter paginated job listings |
| `GET` | `/api/jobs/{id}` | Single job detail view |
| `POST` | `/api/ingestion/run` | Manually trigger ingestion run (`?source_type=rss\|api\|mock`) |
| `GET` | `/api/ingestion/status` | Current ingestion pipeline summary & health |
| `GET` | `/api/ingestion/runs` | Paginated audit log of historical ingestion passes |
| `GET` | `/api/health` | Comprehensive system diagnostic check |

---

## 🚀 Production Deployment Guide

### Frontend (Vercel / Netlify)
1. Push repository to GitHub.
2. Import `frontend/` folder into Vercel or Netlify.
3. Set Build Command: `npm run build` and Output Directory: `dist`.
4. Add Environment Variable: `VITE_API_BASE_URL=https://your-backend.onrender.com`.

### Backend (Render / Railway)
1. Create a Python Web Service on Render/Railway.
2. Root Directory: `backend/`.
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Environment Variables:
   - `DATABASE_URL=postgresql://user:pass@ep-xyz.neon.tech/jobflow_db`
   - `CORS_ORIGINS=https://your-frontend.vercel.app`

---

## 📄 Challenge Artifacts

- [`DECISIONS.md`](./DECISIONS.md) — 1-page architectural decisions & AI disclosure.
- [`docs/architecture.md`](./docs/architecture.md) — Structural diagrams & schema specifications.
- [`docs/ingestion-strategy.md`](./docs/ingestion-strategy.md) — Pipeline stages, normalization rules, and deduplication logic.
- [`docs/detection-surface.md`](./docs/detection-surface.md) — Analysis of anti-bot protections and legal compliance.
- [`docs/resilience.md`](./docs/resilience.md) — Failure handling matrix, backoffs, and automated fallback logic.
