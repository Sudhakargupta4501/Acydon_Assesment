import time
import httpx
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.logger import logger

class SafeHttpClient:
    """
    HTTP Client implementing responsible request pacing, exponential backoff,
    transient failure retries, and strict timeout boundaries.
    """
    def __init__(
        self,
        timeout: int = settings.REQUEST_TIMEOUT,
        min_interval: int = settings.MIN_REQUEST_INTERVAL,
        max_retries: int = settings.MAX_RETRIES,
        backoff_factor: float = settings.BACKOFF_FACTOR,
        user_agent: str = "JobFlow-IngestionBot/1.0 (+https://github.com/jobflow/ingestion-demo)"
    ):
        self.timeout = timeout
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.headers = {"User-Agent": user_agent, "Accept": "application/json, application/xml, text/xml, */*"}
        self.last_request_time: float = 0.0

    def _pace_request(self):
        """Enforces minimum interval delay between outgoing requests to prevent rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            sleep_duration = self.min_interval - elapsed
            logger.debug(f"Pacing request: sleeping for {sleep_duration:.2f}s")
            time.sleep(sleep_duration)
        self.last_request_time = time.time()

    def fetch(self, url: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        req_headers = {**self.headers, **(headers or {})}
        attempt = 0

        while attempt <= self.max_retries:
            self._pace_request()
            attempt += 1

            try:
                logger.info(f"Fetching URL (Attempt {attempt}/{self.max_retries + 1}): {url}")
                with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                    response = client.get(url, headers=req_headers)

                # Check if retryable
                if response.status_code in [500, 502, 503, 504, 429]:
                    if attempt > self.max_retries:
                        response.raise_for_status()
                    backoff = self.backoff_factor ** attempt
                    logger.warning(
                        f"Transient HTTP {response.status_code} for {url}. "
                        f"Retrying in {backoff:.1f}s (Attempt {attempt}/{self.max_retries})."
                    )
                    time.sleep(backoff)
                    continue

                response.raise_for_status()
                return response

            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as exc:
                if attempt > self.max_retries:
                    logger.error(f"Network error exhausted retries for {url}: {exc}")
                    raise exc
                backoff = self.backoff_factor ** attempt
                logger.warning(f"Network exception ({exc}) for {url}. Retrying in {backoff:.1f}s...")
                time.sleep(backoff)

            except httpx.HTTPStatusError as exc:
                # Permanent 4xx errors should fail fast without retrying endlessly
                logger.error(f"Permanent HTTP error {exc.response.status_code} for {url}: {exc}")
                raise exc
