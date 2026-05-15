# Discovered Routes & Endpoints

> Most routes are behind Cloudflare challenge and require a browser session.

## Public Routes (Inferred from Sitemap & Source)

| Route | Description |
|-------|-------------|
| `/` | Main feed/home |
| `/sitemap/sitemap.xml` | Sitemap index |
| `/sitemap/posts/...` | Post sitemaps (by year) |
| `/sitemap/users/...` | User profile sitemaps |
| `/sitemap/tags/...` | Tag sitemaps |
| `/sitemap/publications/...` | Publication sitemaps |
| `/sitemap/catalogs/...` | Catalog sitemaps |
| `/sitemap/lists/...` | List sitemaps |
| `/sitemap/removed-posts/...` | Removed post sitemaps |
| `/robots.txt` | Robots.txt |
| `/_/policy/terms/` | Terms of Service (403/CF protected) |
| `/_/policy/privacy/` | Privacy Policy (inferred) |

## API Routes (Inferred from GraphQL Apollo setup)

Medium uses Apollo GraphQL. Standard Apollo endpoints:

| Route | Description |
|-------|-------------|
| `/graphql` | Standard GraphQL endpoint |
| `/api/graphql` | Alternative GraphQL path |

## Subdomain Routes

| Subdomain | Route Pattern | Description |
|-----------|--------------|-------------|
| link.medium.com | `/*` | URL shortener (307 redirect) |
| go.medium.com | `/*` | URL shortener (Cloudflare protected) |
| status.medium.com | `/` | Status page |
| help.medium.com | `/*` | Zendesk help center |

## Infrastructure Endpoints

| Path | Description |
|------|-------------|
| `/cdn-cgi/challenge-platform/` | Cloudflare challenge scripts |
| `/_/` | Likely internal route prefix |

## Interesting URL Patterns

- **Post URLs:** `/{username}/{slug-123abc}`
- **User Profiles:** `/@username`
- **Publications:** `/tag-name`, `/publication-name`
- **Lists:** `/@{username}/list/{list-id}`
