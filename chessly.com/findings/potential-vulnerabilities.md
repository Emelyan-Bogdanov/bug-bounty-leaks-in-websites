# Potential Vulnerabilities

## 1. Clickjacking (Missing X-Frame-Options) — Medium

**Severity:** Medium  
**Location:** All pages  
**Description:** The `X-Frame-Options` header is missing from all responses. This allows the site to be embedded in an iframe on attacker-controlled websites, enabling clickjacking attacks.

**Evidence:**
```
HTTP/1.1 200 OK
Server: Vercel
Strict-Transport-Security: max-age=63072000
[No X-Frame-Options header]
```

**Impact:** An attacker could overlay a transparent chessly.com page with their own UI to trick users into clicking buttons on Chessly (e.g., subscribing, deleting account, changing settings).

**Fix:** Add `X-Frame-Options: DENY` or `SAMEORIGIN` header.

---

## 2. Missing Content-Security-Policy (CSP) — Medium

**Severity:** Medium  
**Location:** All pages  
**Description:** No CSP header is set. This increases the risk of XSS attacks as there is no restriction on what scripts can execute.

**Impact:** If an XSS vulnerability is found, the attacker can execute arbitrary JavaScript without CSP restrictions.

**Fix:** Implement a strict CSP.

---

## 3. Permissive CORS Policy — Medium

**Severity:** Medium  
**Location:** All endpoints  
**Description:** `Access-Control-Allow-Origin: *` is set on all responses, including various sub-pages.

**Evidence:**
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: OPTIONS, GET, HEAD
```

**Impact:** Any website can make cross-origin requests to Chessly and read the responses. While the site appears to be a static frontend, if any authenticated API responses are cached or served from the same origin, this could lead to data leakage.

**Fix:** Restrict `Access-Control-Allow-Origin` to trusted origins.

---

## 4. Missing X-Content-Type-Options — Low

**Severity:** Low  
**Location:** All pages  
**Description:** `X-Content-Type-Options: nosniff` is not set, which could allow MIME type sniffing in older browsers.

**Fix:** Add `X-Content-Type-Options: nosniff` header.

---

## 5. User Count Disclosure — Low

**Severity:** Low  
**Location:** Landing page (`/`)  
**Description:** The exact number of registered users (1,244,664) is embedded in the page source via `__NEXT_DATA__`.

**Evidence:**
```json
{"props":{"pageProps":{"count":1244664},"__N_SSG":true}...}
```

**Impact:** Low. Provides business intelligence to competitors.

**Fix:** Round the number or remove from client-side data.

---

## 6. Next.js Build ID Exposure — Low

**Severity:** Low  
**Location:** All pages  
**Description:** The Next.js build ID `-q_n9nB7ZNpVJcPUvaYYi` is exposed in the page source. This allows an attacker to identify the exact build version, which could be used to determine if known vulnerabilities in specific Next.js versions apply.

**Evidence:** Found in `__NEXT_DATA__`, `_buildManifest.js`, and `_ssgManifest.js` URLs.

**Impact:** Very Low. Build IDs change with each deployment.

**Fix:** Use opaque/revisioned build IDs (already done, but still exposed).

---

## 7. Potential Authentication Bypass via Historical Subdomains — Info

**Severity:** Unknown / Needs Testing  
**Location:** `api.stytch.chessly.com` (historical)  
**Description:** Stytch authentication API subdomain was historically in use. If still active, it could be a target for auth bypass, rate limiting issues, or API abuse.

**Note:** Needs further testing (would require active engagement with the target).

---

## 8. Google Tag Manager Custom HTML Injection — Info

**Severity:** Medium (if misconfigured)  
**Location:** GTM container `GTM-5PTDGHQF`  
**Description:** If GTM is configured to allow custom HTML tags or if an attacker gains access to the GTM container, they could inject malicious scripts across the entire site.

**Note:** This is a supply chain risk; depends on Chessly's GTM configuration, which cannot be externally verified.

---

## 9. Discord Server Exposure — Info

**Location:** Footer link to `discord.gg/vdx23sQTdj`  
**Description:** The Discord community server invite is publicly exposed. This could be used for social engineering attacks against users.

---

## 10. Old/Staging Subdomains Might Still Be Active — Info

**Severity:** Needs Testing  
**Description:** Several historical subdomains were found via certificate transparency logs. If any are still responding, they may:
- Run outdated software with known vulnerabilities
- Use weak credentials
- Contain debug endpoints
- Have CORS misconfigured

List: `cag.chessly.com`, `cag-preview.chessly.com`, `web-app-staging.chessly.com`, `feedback.chessly.com`, `gateway.chessly.com`, `gateway-preview.chessly.com`, `gateway-staging.chessly.com`

---

**Disclaimer:** This reconnaissance was performed using only passive/non-intrusive techniques (DNS lookups, public certificate logs, HTTP response analysis, and reading client-side JavaScript). No active scanning, authentication bypass attempts, or data tampering was performed. The findings here should be verified by the target's security team.
