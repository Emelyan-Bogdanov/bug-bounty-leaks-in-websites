# Report #2: Secure-CST Cookie Analysis

**Target**: chess.com
**Severity**: MEDIUM (CVSS 5.5)
**Bounty Range**: $100 - $400
**Date**: 2026-05-15
**Status**: Analysis Phase (requires live testing)

---

## Summary

Chess.com uses a `__Secure-cst` cookie described as an "SWR React Query cache key" or "opaque token." This cookie could potentially be exploited for **cache poisoning** or **session hijacking** depending on how it's validated server-side.

---

## Technical Details

### What We Know
- Cookie name: `__Secure-cst`
- Secure flag: present (Secure prefix enforced)
- Purpose: Likely a cache key for SWR React Query (client-side data fetching library)
- Origin: Set by chess.com server during session

### Potential Attack Vectors

#### 1. Cache Poisoning
If the CST cookie is used as a cache key:
- Attacker modifies CST value
- Server may serve another user's cached data
- Results in data leakage across user sessions

#### 2. Predictable Token
If CST is generated with weak entropy:
- Attacker can guess/brute-force CST values
- Gain access to another user's cached session data

#### 3. Missing Server-Side Validation
If CST is not validated server-side:
- Any random value is accepted
- Could lead to cache collisions or session confusion

---

## Analysis Script

The `exploit/cst_analyzer.py` script performs these tests:

```bash
# Decode and analyze the CST structure
python cst_analyzer.py decode <cst_value>

# Test cookie behavior against live endpoint
python cst_analyzer.py test <cst_value> --url https://chess.com/api/settings --session <session_cookie>
```

### What It Checks
1. **Encoding detection**: Base64, hex, or JWT format
2. **Entropy analysis**: Character distribution and randomness
3. **Cache header inspection**: `cf-cache-status`, `cache-control`, `age`, `x-cache`
4. **Behavioral differences**: Responses with original vs modified vs removed CST

---

## Testing Methodology (Live)

### Step 1: Capture
1. Login to chess.com
2. Open DevTools > Application > Cookies
3. Copy `__Secure-cst` value

### Step 2: Decode
```
cst_analyzer.py decode <cst_value>
```
Check if it's:
- JWT (decode on jwt.io)
- Base64 (contains padding `=`)
- Random hex (all hex chars)
- Structured payload

### Step 3: Behavior Tests
| Test | Cookie | Expected Result |
|------|--------|----------------|
| Baseline | Original `__Secure-cst` | Normal response |
| Modified | `aaaaaaaa...` (same length) | Different response = CST matters |
| Empty | `__Secure-cst=` | Error or fallback |
| Removed | No cookie | Cache miss or error |
| Replayed | Another user's CST | Cache hit with their data = CRITICAL |

### Step 4: Cache Header Analysis
Check response headers:
- `cf-cache-status: HIT` vs `MISS`
- `age: <seconds>` (time cached)
- `x-cache: HIT` vs `MISS`

---

## Evidence So Far

### Cookie Pattern (Hypothetical)
Based on SWR React Query patterns:
```
__Secure-cst=<base64_or_hex_token>
```

### Risk Assessment
- **Cache Key**: If CST is part of the cache key → cache poisoning possible
- **Session Token**: If CST is tied to session → hijacking possible
- **Opaque**: No known decode pattern yet → needs live capture

---

## Impact

1. **Cache Poisoning (Critical)**: Modify CST to serve another user's cached data
2. **Information Disclosure (Medium)**: Leak cached data across sessions
3. **Session Confusion (Medium)**: CST could be used as weak session identifier

---

## CVSS v3 Score: 5.5 (MEDIUM)

| Vector | Value |
|--------|-------|
| Attack Vector (AV) | Network |
| Attack Complexity (AC) | Low |
| Privileges Required (PR) | Low |
| User Interaction (UI) | Required (if victim needs to visit crafted link) |
| Scope (S) | Unchanged |
| Confidentiality (C) | Medium |
| Integrity (I) | Low |
| Availability (A) | None |

*Note: Severity may increase to CRITICAL if cache poisoning is confirmed.*

---

## Remediation

1. **Validate CST server-side** — do not trust client-provided values
2. **Use cryptographic signing** for CST if it must be client-readable
3. **Bind CST to session** — invalidate on logout
4. **Add cache validation** — ensure cached responses are tied to the correct user

---

## Files

- `exploit/cst_analyzer.py` — Cookie analysis and testing script
- `analysis/analysis.md` — Deep analysis
- `analysis/interesting_requests.md` — Request observations
