# Technology Stack

## Frontend

| Technology | Version/Notes |
|------------|---------------|
| **Framework** | Next.js (SSG/pre-rendered pages) |
| **React** | 18.3.1 |
| **UI Engine** | React DOM |
| **Styling** | CSS Modules (hashed class names) |
| **Font** | Inter (self-hosted via Next.js font system) |
| **Build ID** | `-q_n9nB7ZNpVJcPUvaYYi` |

## Backend / Hosting

| Technology | Notes |
|------------|-------|
| **Hosting** | Vercel Edge Network |
| **CDN** | Cloudflare (DNS only with proxy) |
| **Server** | Vercel (identified via `Server: Vercel` header) |
| **Caching** | Vercel Edge Cache (HIT/MISS headers visible) |

## Authentication

| Service | Notes |
|---------|-------|
| **Stytch** | Historically used `api.stytch.chessly.com` |
| **Discord OAuth** | `/link-discord` route exists |

## Payments

| Service | Notes |
|---------|-------|
| **Stripe** | Routes: `/stripe-subscription-confirmation`, `/stripe-subscription-cancelation`, `/membership/[plan]/success` |

## Third-Party Services

| Service | ID/Notes |
|---------|----------|
| **Google Tag Manager** | GTM-5PTDGHQF |
| **Google Workspace** | Email via Google |
| **Vimeo** | `/embed/[vimeoVideoId]` for video embedding |
| **Discord** | discord.gg/vdx23sQTdj |

## Data Fetching

- **SWR** (stale-while-revalidate) for client-side data fetching
- Next.js SSG (Static Site Generation) for public pages
- API routes likely under `/api/` (not directly exposed in client bundles)

## JavaScript Libraries Detected

- `framer-motion` (animations)
- `zustand` (state management)
- `next/dynamic` / `@loadable/component` (code splitting)
