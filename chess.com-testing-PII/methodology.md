# PII Extraction Methodology — Chess.com

---

## Objective

Extract Personally Identifiable Information (PII) from chess.com by exploiting the **UUID v1 IDOR vulnerability** identified in the badge system. The goal is to escalate from informational leakage (MAC address + timestamp) to actual user data exposure (email, username, profile data).

---

## Attack Surface

### Known Vulnerable Endpoints (from recon)
| Endpoint | Method | Potential PII |
|----------|--------|---------------|
| `/api/badge/{uuid}` | GET | Badge data, user ID, maybe email |
| `/api/user/{uuid}` | GET | Username, email, profile data |
| `/api/profile/{uuid}` | GET | Full profile: name, location, bio, avatar |

### Suspected Additional Endpoints
| Endpoint | Why |
|----------|-----|
| `/api/settings` | Account settings may contain email |
| `/api/account` | Account details |
| `/api/v1/user/{uuid}` | Versioned API may lack auth checks |
| `/api/v2/user/{uuid}` | Versioned API may have different ACL |

---

## Methodology

### Phase 1: UUID Harvesting

1. **Register a chess.com account** (free)
2. **Navigate to** `https://chess.com/settings/profile`
3. **Open DevTools > Network** tab
4. **Click on any badge** to select it
5. **Find the API request** containing your badge UUID
6. **Save the UUID** for use in enumeration

### Phase 2: Multi-Node Multi-Endpoint Scanning

Run the PII extractor:
```bash
python pii_extractor.py <your-badge-uuid> \
    --range 50 \
    --cookie "session=YOUR_SESSION_COOKIE" \
    --output results/pii_scan_results.json
```

This will:
1. Decode your UUID to extract timestamp + server MAC
2. Generate neighboring UUIDs across ALL known server nodes
3. Probe multiple endpoints for each generated UUID
4. Scan every response for PII patterns (email, username, display name, phone, etc.)

### Phase 3: Endpoint Discovery

Run the endpoint prober to find which endpoints return PII:
```bash
python endpoint_prober.py https://chess.com <your-uuid> \
    --cookie "session=YOUR_SESSION_COOKIE" \
    --output results/endpoint_probe.json
```

This probes 40+ common API endpoints with your UUID to discover:
- Which endpoints are accessible (status < 400)
- Which endpoints return PII in the response
- The content type and structure of each endpoint

### Phase 4: Response Analysis

The PII scanner uses these detection patterns:

| PII Type | Regex Pattern | Example |
|----------|--------------|---------|
| Email | `[\w.+-]+@[\w.-]+\.[a-z]{2,}` | `user@example.com` |
| Username (JSON) | `"username": "([^"]+)"` | `"ibrahim1990"` |
| Display name | `"display_name": "([^"]+)"` | `"Ibrahim ID Wahman"` |
| Phone | `"phone": "([^"]+)"` | `+212600000000` |
| Location | `"location": "([^"]+)"` | `"Casablanca, Morocco"` |
| Avatar URL | `"avatar": "([^"]+)"` | `https://images.chess.com/...` |
| Auth token | `"token": "([A-Za-z0-9_\-.]{20,})"` | JWT or API key |

### Phase 5: Escalation

If PII is found, try to escalate:
1. **Check PUT/PATCH methods** — Can you modify another user's badge/profile?
2. **Check auth bypass** — Can you access without session cookie?
3. **Mass extraction** — Scan wider ranges (--range 500) for bulk PII
4. **Cross-reference** — Use leaked emails for password reset attacks

---

## Response Code Interpretation

| Status | Meaning | Action |
|--------|---------|--------|
| `200` | **HIT** — Full data returned | Extract all PII, save response |
| `401` | Unauthenticated | Add/fix session cookie |
| `403` | Resource EXISTS but blocked | Note for report (still evidence of broken ACL) |
| `404` | No resource at this UUID | Skip, move to next |
| `429` | Rate limited | Add delays, reduce threads |
| `500` | Server error | Interesting — might be processing edge case |

### 403 vs 404 Boundary (Critical Recon)

From previous fuzzing (`interesting-1.txt`):
- UUIDs with `time_low < threshold` → **404** (no badge yet)
- UUIDs with `time_low >= threshold` → **403** (badge exists, access denied)

This allows us to **count exactly how many badges exist** and **when they were created**.

---

## PII Sensitivity Classification

| PII Type | Sensitivity | Bounty Impact |
|----------|------------|---------------|
| Email address | HIGH | Up to $800 |
| Full name | HIGH | Up to $800 |
| Phone number | CRITICAL | $800-$3000 |
| Physical address | CRITICAL | $800-$3000 |
| Date of birth | HIGH | $400-$800 |
| Avatar/photo | MEDIUM | $200-$400 |
| Username | LOW | $100-$200 |

---

## Data Collection & Storage

All results are saved as JSON in the `results/` directory:
- `pii_extraction_results.json` — Full PII scan with all responses
- `endpoint_probe.json` — Endpoint accessibility scan

---

## Operational Security

1. **Use a dedicated account** — Do not use your personal account
2. **Respect rate limits** — Start with --range 10, increase gradually
3. **Do not access private data** — If you find PII, stop and document it
4. **Report responsibly** — Do not extract mass data without authorization

---

## Tools Overview

| Script | Purpose |
|--------|---------|
| `pii_extractor.py` | Multi-node UUID generation + multi-endpoint PII scanning |
| `endpoint_prober.py` | Probe 40+ endpoints for accessibility and PII leakage |

### Usage Examples

```bash
# Full PII scan with known session
python pii_extractor.py abea117e-2af1-11ee-93f0-1f375626db21 \
    --range 100 \
    --cookie "session=abc123def456" \
    --threads 40 \
    --output results/scan1.json

# Probe endpoints with custom list
python endpoint_prober.py https://chess.com abea117e-... \
    --cookie "session=abc123def456" \
    --threads 30 \
    --output results/endpoints.json

# Dry run - analyze UUID only (no HTTP requests)
python ../chess.com/exploit/uuid_v1_fuzzer.py analyze abea117e-...
```
