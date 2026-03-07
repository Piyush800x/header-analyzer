import requests
from headers import SECURITY_HEADERS


def fetch_headers(url):
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        return resp.headers, resp.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error fetching headers: {e}")
        return None, None


def analyze_headers(headers):
    results = []
    score = 100

    deductions = {
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5
    }

    for header, info in SECURITY_HEADERS.items():
        present = header in headers
        if not present:
            score -= deductions[info["severity"]]

        results.append({
            "header": header,
            "present": present,
            "value": headers.get(header, "MISSING"),
            "severity": info["severity"],
            "description": info["description"],
            "recommendation": info["recommendation"] if not present else None
        })

    return results, max(score, 0)


def get_grade(score):
    if score >= 90:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    else:
        return "F"


def print_results(url, results, score):
    grade = get_grade(score)
    print(f"\n{'='*50}")
    print(f"Analysis for: {url}")
    print(f"Score: {score}/100  |  Grade: {grade}")
    print(f"{'='*50}\n")

    for r in results:
        status = f"PRESENT" if r["present"] else f"MISSING"
        print(f"  {status}  [{r['severity']}]  {r['header']}")
        if not r["present"]:
            print(f"↳ Fix: {r['recommendation']}\n")


if __name__ == "__main__":
    url = input("Enter URL to analyze (e.g. https://example.com): ").strip()
    headers, status = fetch_headers(url)

    if headers:
        results, score = analyze_headers(headers)
        print_results(url, results, score)
