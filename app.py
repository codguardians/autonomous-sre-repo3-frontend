from flask import Flask, jsonify, render_template
import os
import requests

app = Flask(__name__)

API_URL = os.environ.get("BACKEND_API_URL", "http://localhost:8000")


@app.route("/")
def index():
    return render_template("index.html", api_url=API_URL)


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "frontend", "version": "1.0.0"})


@app.route("/api/backend-status")
def backend_status():
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"status": "unreachable", "error": str(e)}), 503


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
