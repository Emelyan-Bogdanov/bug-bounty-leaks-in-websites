# Chess.com Attack Suggestions & Methodology

---

## Priority 1: UUID v1 IDOR Exploitation

### Step-by-Step

1. **Create a chess.com account** (free)
2. **Extract badge UUID**: Go to `/settings/profile`, DevTools > Network, click badge, find UUID in API request
3. **Confirm v1**: `uuid.UUID(uuid_str).version == 1`
4. **Decode server info**: Extract MAC + timestamp from UUID
5. **Generate neighbors**: Shift timestamp +/- 50-500 steps (100ns each), keep same node
6. **Enumerate**: Fire GET requests to `/api/badge/{generated_uuid}`
7. **Analyze**: 200 = IDOR confirmed (different user data), 403 = exists but blocked, 404 = none

### Fuzzing Strategy
- Start small (+/-10), expand incrementally
- Use multiple starting UUIDs (different badges you own)
- Test different clock sequences if multiple exist
- Test GET and PUT/PATCH methods

---

## Priority 2: CST Cookie Analysis

### Testing Approach
1. Capture `__Secure-cst` from authenticated session
2. Decode (base64, hex, JWT)
3. Compare across browsers/devices
4. Reuse another user's cst value
5. Modify cst, observe response changes
6. Remove cst, check cache behavior

### If CST is a cache key:
- Change cst value -> if response = another user's data -> CRITICAL cache poisoning

---

## Priority 3: IDOR in Other Resources

If badge UUIDs are v1, check these too:
- User profile IDs
- Game IDs, Tournament IDs
- Article IDs, Forum post IDs
- Puzzle IDs, Lesson IDs

---

## Priority 4: Rate Limiting Tests
- Badge selection endpoint: send 100 rapid requests
- Signup endpoint, password reset, profile updates

---

## Priority 5: Subdomain Recon
- Try: admin, dev, staging, beta, test, api
- Check for: exposed .git, debug endpoints, admin panels, .env files

---

## Priority 6: Authentication Bypass
- Access `/api/badge/{uuid}` without auth cookie
- Try with modified/deleted session
- Try assigning premium badges via IDOR
- Check CSRF protection on badge selection

---

## Priority 7: Information Disclosure
- Server version headers
- Error messages with stack traces
- CORS misconfiguration
- Exposed S3 buckets or CDN origins

---

## Tools (in exploit/ directory)
1. `uuid_v1_fuzzer.py` - UUID generation + enumeration
2. `cst_analyzer.py` - CST cookie analysis
3. `subdomain_scanner.py` - Subdomain discovery
