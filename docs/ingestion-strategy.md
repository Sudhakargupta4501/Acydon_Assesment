# Ingestion Strategy & Pipeline Design

## Pipeline Workflow

Every ingestion execution follows a 6-stage lifecycle:

```text
┌─────────┐    ┌──────────┐    ┌────────────┐    ┌───────────┐    ┌──────────────┐    ┌───────┐
│  FETCH  │ ──>│  PARSE   │ ──>│ NORMALIZE  │ ──>│ VALIDATE  │ ──>│ DEDUPLICATE  │ ──>│ STORE │
└─────────┘    └──────────┘    └────────────┘    └───────────┘    └──────────────┘    └───────┘
```

---

## 1. Source Adapter Abstraction
The `JobSource` abstract base class decouples fetching mechanisms from pipeline stages.

```python
class JobSource(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str: pass

    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]: pass
```

Concrete implementations:
- `RSSJobSource`: Standard RSS 2.0 / Atom feed parser utilizing `feedparser` and `SafeHttpClient`.
- `APIJobSource`: Consumes REST JSON endpoints with dynamic schema detection.
- `MockJobSource`: Provides deterministic datasets for testing duplicate suppression and schema drift errors.

---

## 2. Pacing & Exponential Backoff
The `SafeHttpClient` wraps outgoing requests to protect public servers:
- **Rate Pacing:** Enforces a configurable `MIN_REQUEST_INTERVAL` (default 2 seconds) between consecutive outbound requests.
- **Exponential Backoff:** Retries transient status codes (500, 502, 503, 504, Timeout) using $T_{\text{wait}} = \text{BACKOFF\_FACTOR}^{\text{attempt}}$.
- **Fail Fast:** 4xx client errors (401, 403, 404) trigger immediate fast failure without wasteful retries.

---

## 3. Field Normalization Rules
Data normalizers transform raw input into clean canonical types:
- **Work Mode:** Maps locations containing "Remote", "WFH", "Anywhere" or raw flags to boolean `remote = True`.
- **Employment Type:** Maps variations ("FULL_TIME", "FT", "contractor", "freelance") to standard categories ("Full-time", "Contract", "Part-time", "Internship").
- **Dates:** Parses RFC 2822 (RSS), ISO 8601, Unix timestamps, and falls back to UTC `now()`.
- **Fingerprinting:** Computes SHA-256 hash: $\text{SHA256}(\text{title} \parallel \text{company} \parallel \text{location} \parallel \text{source\_url})$.

---

## 4. Deduplication Logic
Deduplication is executed in 2 layers:
1. **Primary Key Match:** Checks `source + external_id` against current batch memory and database indexes.
2. **Fingerprint Match:** Checks SHA-256 `content_hash` to suppress identical job postings across different feed syndications.
