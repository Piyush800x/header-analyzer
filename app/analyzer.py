import requests
from urllib.parse import urlparse
from app.headers import SECURITY_HEADERS, calculate_grade


def normalize_url(url: str) -> str:
    """Ensure URL has a scheme."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def validate_url(url: str) -> tuple[bool, str]:
    """Validate the URL format."""
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "Invalid URL: Missing domain"
        if parsed.scheme not in ("http", "https"):
            return False, "Invalid URL: Must use http:// or https://"
        return True, ""
    except Exception as e:
        return False, f"Invalid URL: {str(e)}"


def fetch_headers(url: str, timeout: int = 10) -> tuple[dict | None, int | None, str | None]:
    """
    Fetch HTTP headers from a URL.
    Returns: (headers_dict, status_code, error_message)
    """
    try:
        resp = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={"User-Agent": "HeaderSecurityAnalyzer/1.0"}
        )
        return dict(resp.headers), resp.status_code, None
    except requests.exceptions.SSLError:
        return None, None, "SSL certificate error. The site may have an invalid certificate."
    except requests.exceptions.ConnectionError:
        return None, None, "Could not connect to the server. Check if the URL is reachable."
    except requests.exceptions.Timeout:
        return None, None, f"Request timed out after {timeout} seconds"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching headers: {e}")
        return None, None


def analyze(url: str) -> dict:
    """
    Main analysis function. Returns a structured result dict.
    """
    url = normalize_url(url)

    valid, error = validate_url(url)
    if not valid:
        return {"success": False, "error": error}

    headers, status_code, error = fetch_headers(url)
    if error:
        return {"success": False, "error": error}

    results = []
    total_points = sum(h["points"] for h in SECURITY_HEADERS.values())
    earned_points = 0

    for header_name, info in SECURITY_HEADERS.items():
        # Case-insensitive header lookup
        header_value = None
        for key, val in headers.items():
            if key.lower() == header_name.lower():
                header_value = val
                break

        present = header_value is not None
        if present:
            earned_points += info["points"]

        results.append({
            "header": header_name,
            "present": present,
            "value": header_value if present else None,
            "severity": info["severity"],
            "description": info["description"],
            "recommendation": None if present else info["recommendation"],
            "docs": info["docs"],
            "points": info["points"]
        })

    score = round((earned_points / total_points) * 100)
    grade = calculate_grade(score)

    # Sort: missing HIGH first, then MEDIUM, then LOW; present ones last
    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    results.sort(key=lambda x: (x["present"], severity_order[x["severity"]]))

    missing = [r for r in results if not r["present"]]
    present = [r for r in results if r["present"]]

    return {
        "success": True,
        "url": url,
        "status_code": status_code,
        "score": score,
        "grade": grade,
        "headers_present": len(present),
        "headers_missing": len(missing),
        "total_headers_checked": len(results),
        "results": results,
        "summary": {
            "high_risk_missing": sum(1 for r in missing if r["severity"] == "HIGH"),
            "medium_risk_missing": sum(1 for r in missing if r["severity"] == "MEDIUM"),
            "low_risk_missing": sum(1 for r in missing if r["severity"] == "LOW"),
        }
    }
