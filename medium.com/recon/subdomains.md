# Subdomain Enumeration

## Confirmed Active

| Subdomain | HTTP Status | Notes |
|-----------|-------------|-------|
| medium.com | Cloudflare Challenge | Main site |
| www.medium.com | Cloudflare Challenge | Same as main |
| api.medium.com | Cloudflare Challenge | Internal API |
| blog.medium.com | Cloudflare Challenge | Blog |
| m.medium.com | Cloudflare Challenge | Mobile version |
| stats.medium.com | Cloudflare Challenge | Analytics/Stats |
| cdn.medium.com | Cloudflare | CDN |
| static.medium.com | Cloudflare | Static assets |
| cdn-client.medium.com | Cloudflare | Client-side assets (JS/CSS) |
| lite.medium.com | Cloudflare | Lite version of the site |
| policy.medium.com | Cloudflare | Policy pages |
| developer.medium.com | Cloudflare | Developer docs |
| link.medium.com | 307 Redirect | URL shortener |
| status.medium.com | 200 | Status page |
| go.medium.com | 403 | URL shortener (go.medium.com) |
| help.medium.com | Zendesk | CNAME to medium.zendesk.com |

## Discovered from crt.sh Certificate Logs

| Subdomain | Notes |
|-----------|-------|
| *.medium.com | Wildcard cert |
| 37114207.mail.medium.com | Mail tracking subdomain |
| cdn-audio-1.medium.com | Audio CDN |
| cdn-videos.medium.com | Video CDN |
| cdn-videos-1.medium.com | Video CDN |
| jss.medium.com | JavaScript service? |
| read.medium.com | Reading mode |
| url104.mail.medium.com | Email tracking pixel |
| url2204.mail.medium.com | Email tracking pixel |
| url9532.mail.medium.com | Email tracking pixel |
| elonmusk--medium.com | Parody/spam domain (unrelated) |
| voyant--medium.com | Unrelated domain |

## Build/Monitoring Infrastructure

| Domain | Purpose |
|--------|---------|
| stats.medium.build | Build metrics/sourcemaps (found in JS sourceMappingURL) |

## High-Value Targets for Testing

1. **link.medium.com** — URL shortener (redirects, SSRF, open redirect)
2. **go.medium.com** — URL shortener (403 but worth testing)
3. **api.medium.com** — Internal API (auth bypass, rate limiting)
4. **cdn-audio-1.medium.com / cdn-videos.medium.com** — User-uploaded content (SSRF, path traversal if any)
5. **jss.medium.com** — Unknown purpose
6. **developer.medium.com** — API docs
