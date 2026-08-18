# JobFlow System Architecture

## Overview

JobFlow is a production-grade, full-stack Job Listing Data Ingestion & Monitoring Dashboard built with Python (FastAPI), SQLAlchemy, Pydantic, and React (Vite + Tailwind CSS).

```mermaid
flowchart TD
    subgraph External Data Sources
        RSS[Public RSS Feed]
        API[Public REST API]
        MOCK[Sandbox Mock Source]
    end

    subgraph Backend Ingestion Engine (FastAPI)
        Adapter[Source Adapter Interface]
        Client[Safe HTTP Client & Retry]
        Norm[Data Normalizer]
        Val[Pydantic Validator]
        Dedupe[SHA-256 Deduplicator]
        Pipe[Pipeline Orchestrator]
        Sched[APScheduler Cron Task]
    end

    subgraph Storage Layer
        DB[(PostgreSQL / SQLite)]
    end

    subgraph Web Dashboard (React + Vite)
        Dash[Metrics & Search Dashboard]
        IngestPage[Live Pipeline Status]
    end

    RSS --> Adapter
    API --> Adapter
    MOCK --> Adapter
    Adapter --> Client
    Client --> Pipe
    Pipe --> Norm
    Norm --> Val
    Val -->|Valid| Dedupe
    Val -->|Malformed| DB
    Dedupe -->|Unique| DB
    Sched -->|Triggers| Pipe
    DB <--> FastAPI APIs
    FastAPI APIs <--> Dash
    FastAPI APIs <--> IngestPage
```

---

## Data Models

### 1. `Job` Model (`jobs` table)
- `id` (UUID string, Primary Key)
- `external_id` (Indexed string)
- `title` (Indexed string)
- `company` (Indexed string)
- `location` (Indexed string)
- `description` (Text)
- `employment_type` (String: Full-time, Part-time, Contract, Internship)
- `salary` (String)
- `source` (Indexed string)
- `source_url` (Text)
- `posted_at` (DateTime)
- `collected_at` (DateTime)
- `skills` (JSON array)
- `remote` (Indexed boolean)
- `status` (Active / Archived)
- `content_hash` (Indexed SHA-256 string, Unique)

### 2. `IngestionRun` Model (`ingestion_runs` table)
- `id` (UUID string, Primary Key)
- `source` (String)
- `started_at` (DateTime)
- `completed_at` (DateTime)
- `status` (running, success, partial_success, failed)
- `records_fetched` (Integer)
- `records_inserted` (Integer)
- `records_skipped` (Integer)
- `records_failed` (Integer)
- `error_message` (Text)

### 3. `IngestionError` Model (`ingestion_errors` table)
- `id` (Integer Primary Key)
- `run_id` (Indexed string)
- `raw_record` (Text snippet)
- `error_reason` (Text)
- `created_at` (DateTime)
