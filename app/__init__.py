from dotenv import load_dotenv
from flask import Flask, jsonify
from app.database import init_db
from app.routes import register_routes
from app.security import check_malicious_payloads

def create_app():
    load_dotenv()
    app = Flask(__name__)
    init_db(app)
    from app import models  # noqa: F401
    register_routes(app)

    app.before_request(check_malicious_payloads)

    @app.route("/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Resource not found"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(error="Internal server error"), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(error="Method not allowed"), 405

    return app
