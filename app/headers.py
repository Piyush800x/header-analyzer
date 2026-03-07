SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "description": "Prevents XSS by controlling which resources the browser is allowed to load.",
        "severity": "HIGH",
        "points": 20,
        "recommendation": "Add: Content-Security-Policy: default-src 'self'",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"
    },
    "Strict-Transport-Security": {
        "description": "Forces browsers to use HTTPS for all future requests.",
        "severity": "HIGH",
        "points": 20,
        "recommendation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security"
    },
    "X-Frame-Options": {
        "description": "Protects against clickjacking by controlling if the page can be embedded in iframes.",
        "severity": "MEDIUM",
        "points": 15,
        "recommendation": "Add: X-Frame-Options: DENY",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options"
    },
    "X-Content-Type-Options": {
        "description": "Prevents browsers from MIME-sniffing a response away from the declared content-type.",
        "severity": "MEDIUM",
        "points": 15,
        "recommendation": "Add: X-Content-Type-Options: nosniff",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options"
    },
    "Referrer-Policy": {
        "description": "Controls how much referrer information is included with requests.",
        "severity": "LOW",
        "points": 10,
        "recommendation": "Add: Referrer-Policy: strict-origin-when-cross-origin",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy"
    },
    "Permissions-Policy": {
        "description": "Restricts which browser features and APIs can be used.",
        "severity": "LOW",
        "points": 10,
        "recommendation": "Add: Permissions-Policy: geolocation=(), microphone=(), camera=()",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy"
    },
    "X-XSS-Protection": {
        "description": "Legacy XSS filter for older browsers (not needed if CSP is set).",
        "severity": "LOW",
        "points": 5,
        "recommendation": "Add: X-XSS-Protection: 1; mode=block",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection"
    },
    "Cache-Control": {
        "description": "Controls caching behavior to prevent sensitive data from being cached.",
        "severity": "LOW",
        "points": 5,
        "recommendation": "Add: Cache-Control: no-store for sensitive pages",
        "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control"
    }
}


def calculate_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 55:
        return "C"
    elif score >= 35:
        return "D"
    else:
        return "F"
