from flask import Blueprint, jsonify, request
from app.analyzer import analyze

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.route("/analyze", methods=["POST"])
def analyze_url():
    """
    Analyze HTTP security headers for a given URL. 

    Request body (JSON): 
        {
            "url": "https://example.com"
        }

    Returns:
        JSON with score, grade, and per-header analysis.
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON with a 'url' field."
        }), 400

    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "The 'url' field is required and cannot be empty."
        }), 400

    if len(url) > 2048:
        return jsonify({
            "success": False,
            "error": "URL is too long (max 2048 characters)."
        }), 400

    result = analyze(url)

    if not result.get("success"):
        return jsonify(result), 422

    return jsonify(result), 200


@analyze_bp.route("/analyze", methods=["GET"])
def analyze_url_get():
    """
    Analyze via GET with ?url= query parameter for quick testing.
    """

    url = request.args.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "Query parameter 'url' is required. Example: /api/v1/analyze?url=https://example.com"
        }), 400

    if len(url) > 2048:
        return jsonify({
            "success": False,
            "error": "URL is too long (max 2048 characters)."
        })

    result = analyze(url)

    if not result.get("success"):
        return jsonify(result), 422

    return jsonify(result), 200
