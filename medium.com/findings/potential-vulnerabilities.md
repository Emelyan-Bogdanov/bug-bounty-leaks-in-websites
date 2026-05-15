# Potential Vulnerabilities

> **Note:** Medium has a strong security posture (Cloudflare WAF, comprehensive headers, CSP with nonces). The following are areas worth deeper investigation.

---

## 1. Apollo GraphQL Endpoint — Needs Testing

**Severity:** Potentially High  
**Location:** `/graphql` or `/api/graphql` (inferred from `__APOLLO_STATE__`)  
**Description:** Medium uses Apollo Client on the frontend. If the GraphQL endpoint is not properly secured, it could be vulnerable to:

- **Introspection queries** (data schema exposure)
- **Batching attacks** (rate limit bypass)
- **Field suggestion** (enables discovery)
- **Authorization bypass** (accessing data without proper permissions)
- **Deep query nesting** (DoS via complex queries)

**Testing approach:**
```graphql
# Test introspection
query { __schema { types { name } } }

# Check if endpoint is publicly accessible
POST /graphql with Content-Type: application/json
```

---

## 2. URL Shortener Misuse (link.medium.com)

**Severity:** Medium  
**Location:** `link.medium.com` (307 redirect), `go.medium.com` (403)  
**Description:** URL shorteners can be abused for:

- **Open redirect** — redirecting to malicious sites
- **SSRF** — if internal redirects are possible
- **Phishing** — masking malicious URLs behind medium.com domain
- **Path traversal** — if shortener has admin paths

**Testing approach:** Register redirects and test for open redirect patterns.

---

## 3. Cloudflare Challenge Bypass

**Severity:** Medium  
**Description:** While Cloudflare challenge is effective, potential bypass vectors include:

- **API endpoints not behind challenge** (direct access to `api.medium.com`)
- **HTTP/2 downgrade attacks**
- **IP whitelist bypass** (Cloudflare Workers/origin IP discovery)

---

## 4. Subdomain Takeover Potential

**Severity:** Medium  
**Description:** Historical subdomains found in crt.sh logs may have been decommissioned without removing DNS records. Worth checking:

- `jss.medium.com` — Unknown purpose, could be dangling
- `read.medium.com` — If deprecated, may be takeover-able
- Subdomains with `CNAME` to external services (e.g., `help.medium.com → medium.zendesk.com`)

---

## 5. Source Map Exposure on stats.medium.build

**Severity:** Low-Medium  
**Location:** `stats.medium.build` (found in JS sourceMappingURL)  
**Description:** Source maps can reveal original source code with comments, internal API URLs, and development patterns.

**Evidence:** Found in JS file:
```
//# sourceMappingURL=https://stats.medium.build/lite/sourcemaps/instrumentation.bbc70038.chunk.js.map
```

**Testing:** Access other chunk source maps via pattern guessing.

---

## 6. Email Tracking Subdomains (Privacy/Fingerprinting)

**Severity:** Low  
**Location:** `url*.mail.medium.com`, `37114207.mail.medium.com`  
**Description:** Email tracking subdomains used for open/pixel tracking. Potential for:

- Email address enumeration
- Tracking bypass issues
- Redirect abuse

---

## 7. Preloaded State Data Exposure

**Severity:** Low  
**Description:** Medium exposes `__PRELOADED_STATE__` and `__APOLLO_STATE__` in the HTML. If any sensitive data (tokens, user info) leaks into SSR state on public pages, this would be a data leak.

---

## 8. Permission Policy Fingerprinting

**Severity:** Informational  
**Description:** The Permissions-Policy header reveals that `browsing-topics` (Google Topics API) is explicitly disabled with `()`. This confirms Medium deliberately opted out of interest-based advertising via Topics API.

---

## Summary

| # | Finding | Severity | Confidence |
|---|---------|----------|------------|
| 1 | GraphQL endpoint (introspection, abuse) | High | Medium |
| 2 | URL shortener abuse (open redirect) | Medium | Medium |
| 3 | Cloudflare challenge bypass | Medium | Low |
| 4 | Subdomain takeover (historical) | Medium | Low |
| 5 | Source map exposure | Low-Medium | Confirmed |
| 6 | Email tracking/privacy | Low | Confirmed |
| 7 | Preloaded state data leak | Low | Low |
| 8 | Permission policy fingerprinting | Info | Confirmed |

---

**Disclaimer:** This reconnaissance was performed using passive/non-intrusive techniques (DNS lookups, public certificate logs, HTTP response analysis, client-side JS reading). No active scanning, authentication bypass attempts, or data tampering was performed.
