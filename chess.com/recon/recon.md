# Chess.com Reconnaissance Report

**Date**: 2026-05-15
**Target**: chess.com and subdomains
**Program**: HackerOne Bug Bounty (bounties up to $4000)

---

## Subdomain Enumeration

### Known Subdomains (from prior recon)

| Subdomain | Status | IPs | Notes |
|-----------|--------|-----|-------|
| `www.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Main site |
| `chess.com` | RESOLVED | 104.18.x.x | Root domain |
| `api.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | API endpoint |
| `admin.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Admin panel |
| `assets.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Static assets |
| `blog.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Blog |
| `events.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Events |
| `live.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Live streaming |
| `preview.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Preview |
| `shop.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Shop |
| `support.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Support |
| `tracking.chess.com` | RESOLVED | 104.18.x.x (5 IPs) | Tracking/analytics |
| `staging.chess.com` | NXDOMAIN | - | Not found (may use different naming) |
| `dev.chess.com` | NXDOMAIN | - | Not found |
| `cdn.chess.com` | NXDOMAIN | - | Not found (likely behind Cloudflare) |

All resolved subdomains point to **Cloudflare** (104.18.x.x range). The same 5 IPs are load-balanced across all services.

### Resolved Subdomains (Detailed)
- **api.chess.com** — Primary API endpoint (relevant for badge UUID exploitation)
- **admin.chess.com** — May have weaker security, worth deeper investigation
- **preview.chess.com** — Preview/staging environment (potential for weaker controls)
- **shop.chess.com** — E-commerce functionality
- **live.chess.com** — Live streaming features
- **tracking.chess.com** — Analytics/tracking

### Recommended Additional Subdomain Discovery

```bash
# Using common wordlists
# Try: dev, api, staging, admin, cdn, static, assets, blog, forum,
#       support, help, status, mail, mx, ns1, ns2, vpn, remote,
#       jenkins, git, jira, confluence, wiki, docs, beta, test

# Tools to use:
# - subfinder
# - amass
# - assetfinder
# - dnsx
# - httpx
```

---

## Endpoint Discovery

### Known Endpoints (from UUID v1 analysis)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/badge/{uuid}` | GET | Read badge info |
| `/api/badge/{uuid}` | PUT/PATCH | Assign/update badge |
| `/api/user/{uuid}` | GET | User profile |
| `/api/profile/{uuid}` | GET | Profile settings |
| `/settings/profile` | GET | Profile settings page |

### Endpoints to Fuzz

```
/api/
/api/v1/
/api/v2/
/api/user/
/api/profile/
/api/badge/
/api/settings/
/api/account/
/api/notifications/
/api/games/
/api/tournaments/
/api/leaderboard/
/api/streamer/
/api/club/
/api/forum/
/api/blog/
/api/lesson/
/api/coach/
/api/puzzle/
/api/article/
/graphql
/api/graphql
```

---

## Technology Stack (Recon)

### From UUID Analysis
- **Backend**: At least 2 server instances (nodes `ad813d4cf413` and `5309306aceef`)
- **UUID Generation**: Python `uuid.uuid1()` or similar v1 implementation
- **API Style**: RESTful `/api/{resource}/{id}` pattern

### Known Tech Stack (from public info)
- Frontend: React/Next.js
- API: REST + possibly GraphQL
- CDN: Cloudflare or similar
- Real-time: WebSocket for live games
- Caching: SWR React Query (from `__Secure-cst` cookie analysis)

### Cookie Analysis

| Cookie | Purpose | Security |
|--------|---------|----------|
| `__Secure-cst` | SWR cache key / opaque token | Needs analysis |
| `session` | Auth session | Standard |
| `__cfduid` | Cloudflare | Standard |

---

## Infrastructure Fingerprinting

### Server Nodes Detected (from UUID v1)

**Node 1**: `ad:81:3d:4c:f4:13`
**Node 2**: `53:09:30:6a:ce:ef`

These are MAC addresses embedded in UUID v1, confirming:
- Horizontal scaling (multiple servers)
- No MAC privacy/randomization
- UUID generation timestamp = July 2023

### Attack Surface Summary

1. **UUID v1 IDOR** on badges/profile - PREDICTABLE IDs
2. **Secure-CST cookie** - potential cache poisoning
3. **Rate limiting** - needs testing on badge endpoints
4. **Subdomain takeover** - check staging/dev environments
5. **Information disclosure** - UUIDs leak server MAC + timestamps
