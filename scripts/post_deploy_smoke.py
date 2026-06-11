#!/usr/bin/env python3
"""
Dealix Post-Deploy Smoke Test
Checks key pages and API health after deployment.
"""

import argparse
import sys
import urllib.request

PAGES = [
    "/",
    "/sales-machine",
    "/lead-engine",
    "/offers",
    "/pricing",
    "/command-center",
    "/api/health/commercial-os",
]

def check(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "DealixSmoke/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"  FAIL {url} — {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    results = []
    for path in PAGES:
        url = f"{base}{path}"
        ok = check(url)
        results.append((path, ok))
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {url}")

    all_pass = all(ok for _, ok in results)
    if all_pass:
        print("\n[PASS] Post-deploy smoke test complete.")
        sys.exit(0)
    else:
        print("\n[FAIL] Some endpoints did not respond 200 OK.")
        sys.exit(1)

if __name__ == "__main__":
    main()
