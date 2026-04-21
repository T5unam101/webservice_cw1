import argparse
import json
import sys
import time
from urllib import error, parse, request


DEFAULT_BASE_URL = "https://webservice-cw1.onrender.com"
"Because of the network connection issue, the operation will fail." 
"In such cases, it will retry three times. (In fact, it's not because of network issues that it won't fail.)"

def fetch_json(url: str, timeout: int = 20):
    req = request.Request(
        url,
        method="GET",
        headers={"User-Agent": "cities-api-smoke-test/1.0"},
    )
    with request.urlopen(req, timeout=timeout) as resp:
        status = resp.status
        body = resp.read().decode("utf-8")
        data = json.loads(body) if body else None
        return status, data


def run_test(name: str, url: str, validator, retries: int, retry_delay: float):
    for attempt in range(1, retries + 1):
        try:
            status, data = fetch_json(url)
            ok = validator(status, data)
            if ok:
                suffix = f" (attempt {attempt})" if attempt > 1 else ""
                print(f"[PASS] {name}: {status}{suffix}")
                return True
            print(f"[FAIL] {name}: unexpected response {status} {data}")
            return False
        except error.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
            except Exception:
                body = "<unreadable>"
            print(f"[FAIL] {name}: HTTP {e.code} {body}")
            return False
        except error.URLError as e:
            # Intermittent network resets (e.g., WinError 10054) are retried.
            if attempt < retries:
                print(
                    f"[RETRY] {name}: network error on attempt {attempt}/{retries} -> {e}"
                )
                time.sleep(retry_delay * attempt)
                continue
            print(f"[FAIL] {name}: network error after {retries} attempts -> {e}")
            return False
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            return False
    return False


def main():
    parser = argparse.ArgumentParser(description="Smoke test Cities API endpoints.")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="API base URL, e.g. http://127.0.0.1:8000",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of retries for transient network errors (default: 3).",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=1.0,
        help="Base seconds between retries, with linear backoff (default: 1.0).",
    )
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    tests = [
        (
            "health",
            f"{base}/health",
            lambda s, d: s == 200 and isinstance(d, dict) and d.get("status") == "ok",
        ),
        (
            "cities list",
            f"{base}/cities?skip=0&limit=3",
            lambda s, d: s == 200 and isinstance(d, list),
        ),
        (
            "countries list",
            f"{base}/countries?skip=0&limit=3",
            lambda s, d: s == 200 and isinstance(d, list),
        ),
        (
            "cities per country analytics",
            f"{base}/analytics/cities-per-country?limit=5",
            lambda s, d: s == 200 and isinstance(d, list),
        ),
        (
            "countries by continent analytics",
            f"{base}/analytics/countries-by-continent",
            lambda s, d: s == 200 and isinstance(d, list),
        ),
        (
            "nearest city",
            f"{base}/cities/nearest?{parse.urlencode({'city_name': 'London', 'iso2': 'GB'})}",
            lambda s, d: s == 200 and isinstance(d, dict) and "nearest_city" in d,
        ),
    ]

    print(f"Testing API at: {base}")
    results = [
        run_test(name, url, validator, args.retries, args.retry_delay)
        for name, url, validator in tests
    ]
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"\nResult: {passed}/{total} tests passed.")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
