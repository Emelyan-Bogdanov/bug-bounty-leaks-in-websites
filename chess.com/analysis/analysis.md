# Chess.com Vulnerability Analysis

---

## 1. UUID v1 IDOR on Badge System

### Severity: CRITICAL (CVSS 8.6)

### Finding
Chess.com uses **UUID version 1** (time-based) for badge identifiers in profile settings (`/settings/profile`). UUID v1 encodes:
- **Exact timestamp** of generation (60 bits)
- **MAC address** of the server (48 bits)
- **Clock sequence** for collision avoidance (14 bits)

### Impact
1. **IDOR**: Enumerate neighboring UUIDs to access other users' badge data
2. **Info Disclosure**: Server MAC addresses + exact generation timestamps leaked
3. **User Enumeration**: 403 vs 404 response diff identifies valid resources

### Evidence
- 4 UUIDs collected from July 2023 (`leaks/chess.com/saved uuids.txt`)
- Two server nodes detected: `ad813d4cf413` and `5309306aceef`
- Fuzzing results show 403/404 boundary patterns (`bugs/interesting-1.txt`)
- Transition from 404 to 403 responses confirms resource existence

### UUID Breakdown (sample: `abea117e-2af1-11ee-93f0-1f375626db21`)
```
abea117e  -  time_low      (32 bits - lowest timestamp bits)
2af1      -  time_mid      (16 bits - middle timestamp)
11ee      -  version+time_hi (4 bit version = 1, 12 bit time_hi)
93f0      -  variant+clock_seq (2 bit variant, 14 bit clock_seq)
1f375626db21 - node       (48 bit MAC address)
```

### UUID v1 Decoding
```python
import uuid
from datetime import datetime, timezone

u = uuid.UUID("abea117e-2af1-11ee-93f0-1f375626db21")
GREGORIAN_OFFSET = 0x01b21dd213814000
unix_ts = (u.time - GREGORIAN_OFFSET) / 1e7
dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
print(f"Node MAC: {u.node:#014x}, Generated: {dt}")
```

---

## 2. Secure-CST Cookie Analysis

### Severity: MEDIUM (CVSS 5.5)

### What It Is
The `__Secure-cst` cookie is described as:
- "SWR React Query cache key"
- "Opaque token"
- Used in API requests

### Attack Scenarios
1. **Cache Poisoning**: If `cst` is a cache key, manipulating it could serve another user's cached data
2. **Predictable Token**: If generated with weak entropy, it could be guessed
3. **Session Association**: If tied to a session, reusing could leak data

### Testing Plan
1. Capture `cst` from authenticated session
2. Decode (base64? hex? JWT?)
3. Compare across browsers/devices
4. Test reuse of another user's `cst`
5. Test removal/modification for cache behavior

---

## 3. Response Code Analysis (403 vs 404)

### Key Finding
Fuzzing results in `interesting-1.txt` show a clear **403/404 boundary**:
- UUIDs before a certain timestamp → **404** (no resource)
- UUIDs after a certain timestamp → **403** (resource exists, access denied)

This confirms:
- Resources are created sequentially over time
- 403 means the resource EXISTS but we don't have permission (evidence of broken access control)
- 404 means no resource at that timestamp

### Attack Implication
The boundary between 404/403 is at a specific timestamp. UUIDs with time_low around `abea0f94` transition from 404 to 403. This means:
- We can identify EXACTLY when badges were created
- We can count how many badges exist per time window
- We can target specific time ranges for enumeration

---

## 4. HackerOne Program Context

### Scope
- `chess.com` domain only
- Report to: `bounties{at}chesscom{dot}atlassian{dot}net`
- Policy: https://www.chess.com/news/view/chess-com-bug-bounty-policy

### Bounty Payouts

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

### Our Target for UUID v1
- **$200-$400** for IDOR reading others' badge data
- **Up to $800** if PII (email) leaked
- **Up to $800-$3000** if mass user data accessible
- **$100** minimum for info leakage (MAC + timestamp)

---

## 5. Attack Chain Priority

### Chain 1: UUID Enumeration → PII Leakage (HIGHEST PRIORITY)
1. Get own badge UUID from `/settings/profile`
2. Confirm v1 (version field = 1)
3. Decode timestamp + MAC
4. Generate ±50-100 neighboring UUIDs
5. Enumerate `/api/badge/{uuid}` 
6. Check for other users' data (email, username, etc.)
7. Escalate to PUT/PATCH for badge assignment

### Chain 2: Cache Poisoning via CST Cookie
1. Analyze `__Secure-cst` structure
2. Test if modifying it leaks other users' data
3. Test if removing it changes cache behavior

### Chain 3: Staging/Dev Subdomain Recon
1. Fuzz for `staging.chess.com`, `dev.chess.com`
2. Check for weaker security on subdomains
3. Look for debug endpoints, exposed configs
