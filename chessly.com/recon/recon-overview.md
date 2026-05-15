# Recon Overview

## DNS Records

| Type | Value |
|------|-------|
| A | 76.76.21.21 |
| NS | brynne.ns.cloudflare.com, david.ns.cloudflare.com |
| MX | aspmx.l.google.com (priority 1), alt1-4.aspmx.l.google.com (5, 10) |
| TXT | `v=spf1 include:_spf.google.com -all` |
| TXT | google-site-verification (2 entries) |
| SOA | dns.cloudflare.com |

## WHOIS / General

- **IP:** 76.76.21.21
- **Hosting:** Vercel (Edge Network)
- **CDN/DNS:** Cloudflare (behind proxied DNS)
- **Email:** Google Workspace (Gmail)
- **Auth Service:** Stytch (historically used `api.stytch.chessly.com`)

## SSL / TLS

- **HSTS:** Enabled (max-age=63072000 ~ 2 years)
- **Certificate:** Issued by Cloudflare / Let's Encrypt
- **Wildcard cert:** `*.chessly.com`

## Security Headers Status

| Header | Status |
|--------|--------|
| Strict-Transport-Security | ✅ max-age=63072000 |
| Access-Control-Allow-Origin | ⚠️ `*` (wildcard) |
| X-Frame-Options | ❌ Missing (clickjacking) |
| X-Content-Type-Options | ❌ Missing |
| Content-Security-Policy | ❌ Missing |
| X-XSS-Protection | ❌ Missing |
| Referrer-Policy | ❌ Missing |
| Permissions-Policy | ❌ Missing |

## User Count Disclosure

The landing page exposes: **1,244,664 users** have tried Chessly.

This is exposed via `__NEXT_DATA__` in the HTML:
```json
{"props":{"pageProps":{"count":1244664},"__N_SSG":true}...}
```
