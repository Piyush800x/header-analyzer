from flask import Blueprint, jsonify
import time

health_bp = Blueprint("health", __name__)
START_TIME = time.time()


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for uptime monitoring and load balancers."""
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME),
        "version": "1.0.0"
    })
