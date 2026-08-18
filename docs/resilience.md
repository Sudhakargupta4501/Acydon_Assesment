# Resilience & Error Handling Architecture

## Failure Vectors & Handling Matrix

| Scenario | Potential Impact | System Mitigation Strategy | Result |
| :--- | :--- | :--- | :--- |
| **Source Timeout / Server 503** | Transient network failure | `SafeHttpClient` retries up to `MAX_RETRIES=3` with exponential backoff $2^{\text{attempt}}$s | Recovers automatically if transient; switches to fallback source if exhausted. |
| **Primary Source Down** | Complete failure of primary feed | Pipeline automatically activates configured secondary `FallbackSource` | Ingestion completes with degraded status badge in UI. |
| **Empty Source Response** | 0 records returned | Caught cleanly without exception; logs warning and updates run status | Run completes marked as `success` with 0 records inserted. |
| **Malformed XML/JSON Record** | Schema missing `title` or `company` | `RecordValidator` catches Pydantic error, logs raw record to `ingestion_errors` table | Bad record skipped; remaining batch processes successfully. |
| **Duplicate Syndication** | Same job posted in multiple feeds | `Deduplicator` matches SHA-256 fingerprint hash before DB insert | Duplicate skipped without throwing database constraint error. |
| **Database Disconnection** | DB commit failure | SQLAlchemy rollback executed, transaction safely aborted | Ingestion run logged as `failed` with exact traceback message stored. |

---

## Automatic Fallback Architecture

```text
               ┌────────────────────────┐
               │ Primary Job Source     │
               └───────────┬────────────┘
                           │
                 Fetch Successful?
                 ┌─────────┴─────────┐
                YES                  NO
                 │                   │
                 ▼                   ▼
           Process Batch    ┌────────────────────────┐
                            │ Secondary Fallback     │
                            └───────────┬────────────┘
                                        │
                              Fetch Successful?
                              ┌─────────┴─────────┐
                             YES                  NO
                              │                   │
                              ▼                   ▼
                        Process Batch      Mark Run FAILED
```
