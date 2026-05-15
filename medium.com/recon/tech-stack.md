# Technology Stack

## Frontend (from JS source analysis)

| Technology | Details |
|------------|---------|
| **Framework** | Custom "lite" framework (Progressive Web App) |
| **UI Library** | React (hooks, useSyncExternalStore, etc.) |
| **State Management** | Redux (`window.__PRELOADED_STATE__`) |
| **GraphQL Client** | Apollo Client (`window.__APOLLO_STATE__`) |
| **Build Tool** | Webpack / Loadable Components (chunk-based) |
| **Router** | Custom client-side router |
| **Performance** | Custom PerformanceLogger (LCP, FCP, FID, CLS, INP) |

## Backend / Hosting

| Component | Technology |
|-----------|------------|
| **Hosting** | Cloudflare proxied |
| **Origin Server** | Not directly exposed (behind Cloudflare) |
| **API Protocol** | GraphQL (Apollo) |
| **Edge Cache** | Custom edge caching system |
| **Email** | Amazon SES, SendGrid, Google Workspace |
| **Payments/Tip** | Tipalti (SPF record) |

## CDN & Assets

| Asset Type | CDN |
|------------|-----|
| Client JS/CSS | `cdn-client.medium.com` |
| Audio | `cdn-audio-1.medium.com` |
| Video | `cdn-videos.medium.com`, `cdn-videos-1.medium.com` |
| Static | `static.medium.com`, `cdn.medium.com` |

## JavaScript Libraries Detected

| Library | Purpose |
|---------|---------|
| Redux | State management |
| Apollo Client | GraphQL queries/mutations |
| React | UI components |
| @loadable/component | Code splitting |
| Custom instrumentation | Web Vitals (LCP, FCP, FID, CLS, INP) |

## Monitoring/Build

| Service | URL |
|---------|-----|
| Source Maps | `stats.medium.build` |
| Status Page | `status.medium.com` |
| Edge Cache | Custom edge caching (detected via `__PRELOADED_STATE__`) |

## Sitemap Structure

```
/sitemap/sitemap.xml
  ├── /sitemap/posts/{year}/posts-{year}-{month}-{day}.xml
  ├── /sitemap/users/{year}/users-{year}-{month}-{day}.xml
  ├── /sitemap/tags/{year}/tags-{year}-{month}-{day}.xml
  ├── /sitemap/publications/{year}/publications-{year}-{month}-{day}.xml
  ├── /sitemap/catalogs/{year}/catalogs-{year}-{month}-{day}.xml
  ├── /sitemap/lists/{year}/lists-{year}-{month}-{day}.xml
  └── /sitemap/removed-posts/{year}/removed-posts-{year}-{month}-{day}.xml
```
