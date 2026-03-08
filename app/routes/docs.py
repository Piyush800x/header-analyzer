from flask import Blueprint, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

docs_bp = Blueprint("docs", __name__)

# Route where Swagger UI will be served
SWAGGER_URL = "/api/v1/docs"

# Route that serves the raw openapi.json spec
API_SPEC_URL = "/api/v1/docs/openapi.json"

# Register Swagger UI blueprint from the library
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_SPEC_URL,
    config={
        "app_name": "HTTP Header Security Analyzer",
        "displayRequestDuration": True,
        "tryItOutEnabled": True,
        "defaultModelsExpandDepth": 1,
    }
)


@docs_bp.route("/docs/openapi.json")
def openapi_spec():
    """Serve the OpenAPI JSON spec file."""
    static_dir = os.path.join(os.path.dirname(__file__), "..", "..", "static")
    return send_from_directory(os.path.abspath(static_dir), "openapi.json")
