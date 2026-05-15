# Interesting Requests & Response Analysis

---

## 1. Badge UUID Fuzzing Results

### Source: `leaks/chess.com/bugs/interesting-1.txt`

### Observation

Fuzzing UUIDs around the known badge range showed a clear **403/404 boundary**:

```
[404] abea0f8a-2af1-11ee-93f0-1f375626db21  ← 404 (no resource)
[404] abea0f8b-2af1-11ee-93f0-1f375626db21
...
[404] abea0f94-2af1-11ee-93f0-1f375626db21
[403] abea0f95-2af1-11ee-93f0-1f375626db21  ← 403 (EXISTS but blocked!)
[403] abea0f96-2af1-11ee-93f0-1f375626db21
...
```

### Analysis

The transition from 404 → 403 at `abea0f95` is the EXACT timestamp boundary where badges started existing. This tells us:

1. **Badges were created in sequence starting at a specific time**
2. **403 means the badge exists but we don't have access** → Confirms broken access control
3. **We can determine the exact count of badges per server node**

### UUID Range Analysis
```
Range:    abea0f8a → abea0f95 (before badges existed → after)
Delta:    0xB = 11 steps in time_low
Meaning:  Badges were created at ~11 × 100ns intervals
```

### What This Means for Exploitation
- If we can get ANY user's badge UUID, we can enumerate ALL badges created near that time
- The 403 response is a signal that the UUID is valid - we just need auth bypass
- If we find a UUID that returns 200, we may be able to scan the entire range

---

## 2. Server Node Analysis

### Two Distinct Server Nodes Detected

| UUID | Node (MAC) | Server Instance |
|------|-----------|-----------------|
| `abea117e-2af1-11ee-93f0-1f375626db21` | `1f:37:56:26:db:21` | Server A |
| `abea13cc-2af1-11ee-b8a8-0710e9c93295` | `07:10:e9:c9:32:95` | Server A |
| `abea1624-2af1-11ee-b605-530cf2dfaa9a` | `53:0c:f2:df:aa:9a` | Server B |
| `abea1872-2af1-11ee-9194-9b04a8f3be53` | `9b:04:a8:f3:be:53` | Server B |

### Interesting Pattern
The time_low values are sequential across BOTH servers:
```
abea117e → Server A
abea13cc → Server A
abea1624 → Server B
abea1872 → Server B
```

This suggests **round-robin load balancing** where requests alternate between servers.

---

## 3. Image URL Pattern Analysis

### Source: `leaks/chess.com/sided/build hash for imageprofile .py`

### URL Format
```
{base_url}/{asset_id}.{file_hash}.{width}x{height}{mode}.{signature}@{dpi_scale}x
```

### Example
```
https://example.com/images/510572149.814de8b7.160x160o.53bb7393a62c@2x
```

### Components
| Part | Value | Purpose |
|------|-------|---------|
| asset_id | `510572149` | Numeric asset ID |
| file_hash | `814de8b7` | CRC32/hash of file |
| dimensions | `160x160o` | Width x Height + mode |
| signature | `53bb7393a62c` | HMAC security token |
| dpi_scale | `2x` | Retina multiplier |

### Potential Weaknesses
1. **Predictable asset_id**: Are they sequential? Can we enumerate?
2. **Weak hash**: If `file_hash` is CRC32, it's trivially collidable
3. **Signature reuse**: Same signature across assets?
4. **IDOR**: Can we access other users' uploaded images by changing asset_id?

---

## 4. Request Patterns Observed

### Badge Selection Flow
1. User visits `/settings/profile`
2. Browser loads badge list (probably from JS bundle or API)
3. User clicks badge → triggers request containing UUID
4. API validates badge assignment → updates profile

### Recommended Interception Points
```
GET/PUT /api/badge/{uuid}           - Badge read/assign
GET/PUT /api/user/{uuid}            - User profile
GET/PUT /api/profile/{uuid}         - Profile settings
GET     /api/settings               - Account settings (check CST cookie)
POST    /api/session                - Login
POST    /api/signup                 - Registration
```

---

## 5. Potential Bypass Scenarios

### Auth Bypass on Badge Endpoint
- What if `GET /api/badge/{uuid}` works without auth?
- What if we can use another user's session token?
- What if badges are loaded client-side from a public CDN?

### Premium Badge Assignment
- Can we assign a premium badge to our profile via IDOR?
- Try PUT/PATCH on badge endpoint with different UUID
- Check if badge type is validated server-side

### Cache Poisoning via CST
- If CST is client-generated, we control it
- Test: Change CST, make request, see if we get another user's cached data
- Test: Remove CST, check if we get uncached responses (slower)
