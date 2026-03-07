# 🔒 HTTP Header Security Analyzer API

A production-ready REST API built with Flask that audits any website's HTTP security headers, scores it out of 100, and returns actionable remediation recommendations.

## Features

- ✅ Analyzes 8 critical security headers (CSP, HSTS, X-Frame-Options, and more)
- ✅ Scores sites 0–100 with A–F grading
- ✅ Returns severity-ranked findings (HIGH / MEDIUM / LOW)
- ✅ Built-in rate limiting (30 req/min per IP)
- ✅ CORS enabled for frontend integration
- ✅ Input validation and structured error responses
- ✅ Health check endpoint
- ✅ Docker + Gunicorn ready for production
- ✅ 12 unit tests passing

---

## Quickstart

### Local (Python)
```bash
git clone https://github.com/yourusername/header-analyzer
cd header-analyzer
pip install -r requirements.txt
python run.py
```

### Docker
```bash
docker-compose up --build
```

API is now running at `http://localhost:5000`

---

## API Reference

### `POST /api/v1/analyze`

Analyze a URL via JSON body.

**Request:**
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com",
  "status_code": 200,
  "score": 55,
  "grade": "C",
  "headers_present": 3,
  "headers_missing": 5,
  "total_headers_checked": 8,
  "summary": {
    "high_risk_missing": 1,
    "medium_risk_missing": 2,
    "low_risk_missing": 2
  },
  "results": [
    {
      "header": "Content-Security-Policy",
      "present": false,
      "value": null,
      "severity": "HIGH",
      "description": "Prevents XSS by controlling which resources the browser is allowed to load.",
      "recommendation": "Add: Content-Security-Policy: default-src 'self'",
      "docs": "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP",
      "points": 20
    }
  ]
}
```

### `GET /api/v1/analyze?url=https://example.com`

Quick scan via query parameter — useful for testing.

```bash
curl "http://localhost:5000/api/v1/analyze?url=https://example.com"
```

### `GET /api/v1/health`

Health check for load balancers and uptime monitors.

```json
{
  "status": "healthy",
  "uptime_seconds": 120,
  "version": "1.0.0"
}
```

---

## Headers Checked

| Header | Severity | Points |
|--------|----------|--------|
| Content-Security-Policy | HIGH | 20 |
| Strict-Transport-Security | HIGH | 20 |
| X-Frame-Options | MEDIUM | 15 |
| X-Content-Type-Options | MEDIUM | 15 |
| Referrer-Policy | LOW | 10 |
| Permissions-Policy | LOW | 10 |
| X-XSS-Protection | LOW | 5 |
| Cache-Control | LOW | 5 |

## Grading Scale

| Score | Grade |
|-------|-------|
| 90–100 | A |
| 75–89 | B |
| 55–74 | C |
| 35–54 | D |
| 0–34 | F |

---

## Project Structure

```
header-analyzer/
├── app/
│   ├── __init__.py        # App factory, CORS, rate limiting
│   ├── analyzer.py        # Core analysis logic
│   ├── headers.py         # Header rules and scoring config
│   └── routes/
│       ├── analyze.py     # POST & GET /analyze endpoints
│       └── health.py      # Health check endpoint
├── tests/
│   └── test_api.py        # 12 unit tests
├── run.py                 # Entry point
├── requirements.txt
├── Dockerfile
```

---

## Running Tests

```bash
python3 -m pytest tests/ -v
```

---

## Tech Stack

- **Flask** — web framework
- **Gunicorn** — production WSGI server
- **Docker** — containerization
- **requests** — HTTP header fetching

---

## Skills Demonstrated

- REST API design with Flask Blueprints
- Input validation and structured error handling
- Rate limiting without external dependencies
- CORS configuration
- Production deployment with Gunicorn + Docker
- Security-domain knowledge (OWASP headers)
- Unit testing with Flask test client