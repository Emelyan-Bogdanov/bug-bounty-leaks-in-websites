# Recon Overview

## DNS Records

| Type | Value |
|------|-------|
| A | 162.159.153.4, 162.159.152.4 (Cloudflare) |
| AAAA | 2606:4700:7::a29f:9904, 2606:4700:7::a29f:9804 |
| NS | alina.ns.cloudflare.com, kip.ns.cloudflare.com |
| MX | aspmx.l.google.com (prio 1), alt1-2 (5), aspmx2-3.googlemail.com (10) |
| TXT | v=spf1 include:amazonses.com include:_spf.google.com include:mail.zendesk.com include:sendgrid.net include:spf.tipalti.com include:_spf.psm.knowbe4.com ~all |
| TXT | Multiple domain verification records |

### Domain Verification Records Exposed

These TXT records reveal integrations/services Medium uses:

| Record | Service |
|--------|---------|
| google-site-verification (x5) | Google Search Console |
| apple-domain-verification | Apple |
| dropbox-domain-verification | Dropbox |
| facebook-domain-verification | Facebook |
| openai-domain-verification | OpenAI |
| anthropic-domain-verification | Anthropic |
| cursor-domain-verification | Cursor |
| linear-domain-verification | Linear |
| notion-domain-verification | Notion |
| yahoo-verification-key | Yahoo |

## Hosting & Infrastructure

| Component | Technology |
|-----------|------------|
| **CDN/WAF** | Cloudflare (JS challenge + Turnstile) |
| **DNS** | Cloudflare |
| **Email** | Google Workspace, Amazon SES, SendGrid, Zendesk, Tipalti |
| **SPF record help desk** | Zendesk (`mail.zendesk.com`) |

## Security Headers

| Header | Status | Value |
|--------|--------|-------|
| Strict-Transport-Security | ✅ | max-age=31536000; includeSubDomains; preload |
| X-Frame-Options | ✅ | SAMEORIGIN |
| X-Content-Type-Options | ✅ | nosniff |
| Content-Security-Policy | ✅ | With nonces (Cloudflare managed) |
| Referrer-Policy | ✅ | same-origin |
| Permissions-Policy | ✅ | Extensive restrictions (all `()`) |
| Cross-Origin-Embedder-Policy | ✅ | require-corp |
| Cross-Origin-Opener-Policy | ✅ | same-origin |
| Cross-Origin-Resource-Policy | ✅ | same-origin |
| Origin-Agent-Cluster | ✅ | ?1 |

> **Note:** Medium has excellent security headers. The Cloudflare managed challenge adds a nonce-based CSP on the landing page.

## Interesting Observations

- The site triggers a **Cloudflare JS challenge** on direct/server requests — browser required to pass
- `cf-mitigated: challenge` header confirms Cloudflare challenge mode
- `server-timing` header reveals ray IDs for debugging
- `alt-svc: h3=":443"; ma=86400` — HTTP/3 (QUIC) supported
