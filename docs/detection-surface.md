# Detection Surface & Anti-Bot Protections Analysis

## Conceptual Analysis of Detection Vectors

Automated data collection clients expose several detection vectors when interacting with web platforms:

### 1. Browser & TLS Fingerprinting
- **JA3 / JA4 Signatures:** Headless automation frameworks (Puppeteer, Selenium, Playwright) expose TLS client hello fingerprints that differ significantly from legitimate user browsers (Chrome, Firefox, Safari).
- **HTTP/2 Frame Settings:** Automated HTTP clients often negotiate HTTP/2 parameters or header orderings that reveal non-browser origin.
- **Navigator DOM Artifacts:** `navigator.webdriver`, headless WebGL flags, and canvas rendering artifacts.

### 2. Request Timing & Frequency
- **Burst Pacing:** Unnatural, constant millisecond request intervals signal programmatic scraping.
- **Navigation Patterns:** Direct deep linking to target endpoints without preceding page loads or referrer headers.

### 3. IP Reputation & Proxy Anomaly
- **Datacenter IPs:** Traffic originating from AWS, DigitalOcean, or Hetzner ranges is flagged by Cloudflare/Akamai web application firewalls (WAFs).

---

## Architectural Guardrails & Compliance Rationale

> [!IMPORTANT]
> **Our Live Implementation Strategy:**
> 1. **Zero Evasion:** We explicitly **do NOT** implement TLS spoofing, stealth browser fingerprinting, proxy rotation, or CAPTCHA solving.
> 2. **Permitted Public Feeds:** We restrict data collection to permitted public RSS feeds and public REST APIs designed specifically for syndication.
> 3. **Polite Client Identification:** Outbound requests transmit an explicit identification header: `User-Agent: JobFlow-IngestionBot/1.0 (+https://github.com/jobflow/ingestion-demo)`.
> 4. **Responsible Pacing:** Requests enforce a minimum interval delay of 2.0 seconds.

This approach demonstrates robust systems engineering while fully honoring platform terms of service.
