from flask import Flask, jsonify, request
from collections import defaultdict
import time
from dotenv import load_dotenv
import os

load_dotenv()

_rate_limit_store = defaultdict(list)
RATE_LIMIT_REQUESTS = 30
RATE_LIMIT_WINDOW = 60  # seconds


def is_rate_limited(ip: str) -> bool:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    _rate_limit_store[ip] = [
        timestamp for timestamp in _rate_limit_store[ip] if timestamp > window_start]

    if len(_rate_limit_store[ip]) >= RATE_LIMIT_REQUESTS:
        return True
    _rate_limit_store[ip].append(now)
    return False


def create_app(config=None):
    app = Flask(__name__)

    app.config.update(
        JSON_SORT_KEYS=False,
        SECRET_KEY=os.getenv("SECRET_KEY"),
        TESTING=False
    )

    if config:
        app.config.update(config)

    # Register blueprints
    from app.routes.analyze import analyze_bp
    from app.routes.health import health_bp
    from app.routes.docs import docs_bp, swaggerui_blueprint

    app.register_blueprint(analyze_bp, url_prefix="/api/v1")
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(docs_bp, url_prefix="/api/v1")
    app.register_blueprint(swaggerui_blueprint)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    @app.before_request
    def check_rate_limit():
        if app.config.get("TESTING"):
            return
        if request.method == "OPTIONS":
            return

        ip = request.remote_addr or "unknown"
        if is_rate_limited(ip):
            return jsonify({
                "success": False,
                "error": f"Rate limit exceeded: max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW}s"
            }), 429

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "error": "Endpoint not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "success": False,
            "error": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

    return app
