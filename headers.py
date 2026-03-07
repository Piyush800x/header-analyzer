SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "description": "Prevents XSS by whitelisting content sources.",
        "severity": "HIGH",
        "recommendation": "Add CSP: default-src 'self'"
    },
    "Strict-Transport-Security": {
        "description": "Forces HTTPS connections.",
        "severity": "HIGH",
        "recommendation": "Add HSTS: max-age=31536000; includeSubDomains"
    },
    "X-Frame-Options": {
        "description": "Prevents clickjacking attacks.",
        "severity": "MEDIUM",
        "recommendation": "Set to DENY or SAMEORIGIN"
    },
    "X-Content-Type-Options": {
        "description": "Prevents MIME type sniffing.",
        "severity": "MEDIUM",
        "recommendation": "Set to nosniff"
    },
    "Referrer-Policy": {
        "description": "Controls referrer information leakage.",
        "severity": "LOW",
        "recommendation": "Set to no-referrer or strict-origin"
    },
    "Permissions-Policy": {
        "description": "Restricts access to browser APIs.",
        "severity": "LOW",
        "recommendation": "Define allowed features explicitly"
    }
}
