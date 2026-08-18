# Architectural & Engineering Decisions

This document summarizes the core technical decisions, trade-offs, and transparency disclosures for the **JobFlow Job Listing Data Ingestion Platform** (Acdyon Technologies Challenge — Part 1).

---

## 1. Why this ingestion strategy?

Rather than implementing brittle, high-risk headless browser scraping against anti-bot-protected sites (which violates Terms of Service, risks IP blocks, and breaks unpredictably under UI updates), we selected a **decoupled Adapter Pattern** consuming permitted, low-risk public data sources (`WeWorkRemotely RSS`, `Arbeitnow REST API`, and a configurable `Sandbox Mock Source`).

### Key Benefits:
- **Zero Detection Surface Risk:** Operates strictly within legal, permitted bounds with explicit `User-Agent` identification.
- **High Pipeline Resilience:** Focuses engineering effort on data quality, normalization, Pydantic schema validation, and SHA-256 fingerprint deduplication rather than bypassing CAPTCHAs.
- **Extensible Architecture:** Adding a new job source requires only inheriting from `JobSource` (`fetch_jobs()`) without modifying downstream parser, validator, or storage layers.
- **Responsible Rate Pacing:** Integrated `SafeHttpClient` with exponential backoff and minimum request interval delays (2s default) to prevent server strain.

---

## 2. What trade-off did you make?

### Primary Trade-Off:
**Depth of Data Normalization over Multi-Platform Source Coverage.**

Due to the evaluation timeframe, we prioritized building a **production-ready ETL pipeline architecture** (with robust error recovery, automated fallback handling, database deduplication, and a rich live dashboard) rather than writing 10+ fragile site-specific web scrapers.

### What would be built with 1 additional week?
1. **Dynamic Schema Drift Detection:** Automated alerting when source JSON key distributions shift significantly from baseline expectations.
2. **Distributed Queue Architecture:** Transitioning background jobs from APScheduler to Celery + Redis for multi-worker parallel ingestion scale.
3. **Advanced Entity Resolution:** AI-assisted skills extraction and job classification using fine-tuned embeddings (e.g., mapping "React.js", "React Native", and "ReactJS" into canonical skill graphs).
4. **Webhook & Alert Subscriptions:** Real-time email/Slack alerts for degraded source health or ingestion pipeline failures.

---

## 3. Where did you use AI?

| Stage | AI Usage Description | Review & Verification Method |
| :--- | :--- | :--- |
| **Boilerplate Scaffolding** | Generated initial FastAPI route structures, Pydantic schema declarations, and React Tailwind layout templates. | Hand-reviewed every line of generated code, adjusted field types, and enforced strict Pydantic v2 validation. |
| **Documentation & Diagrams** | Assisted in converting architectural text into clean GitHub Markdown and Mermaid sequence diagrams. | Verified diagram flow against actual code execution paths. |
| **Test Case Generation** | Generated unit test stubs for edge-case string cleaning and invalid schema inputs. | Ran `pytest` backend test suite locally and verified 100% pass rates. |

*All architectural boundaries, deduplication logic, retry backoffs, and UI designs were thoroughly reviewed and tested to ensure production standards.*
