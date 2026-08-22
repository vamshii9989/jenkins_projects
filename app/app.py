"""
Simple Flask application used to demonstrate a full CI/CD pipeline:
Clone -> Build -> Test -> Compile -> Docker Build -> Docker Tag ->
Docker Login -> Docker Push -> Clean Workspace.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint used by Docker HEALTHCHECK / monitoring."""
    return jsonify(status="ok"), 200


@app.route("/add", methods=["GET"])
def add():
    """Add two numbers passed as query params: /add?a=2&b=3"""
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
    except ValueError:
        return jsonify(error="a and b must be numbers"), 400
    return jsonify(result=a + b), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify(message="Simple DevOps demo app is running!"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
