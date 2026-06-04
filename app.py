from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

API_URL = os.environ.get("BACKEND_API_URL", "")

HTML = """<!DOCTYPE html>
<html>
<head>
<title>Autonomous SRE Demo</title>
<style>
body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 16px 0; }
.ok  { color: #059669; font-weight: bold; }
.err { color: #dc2626; font-weight: bold; }
</style>
</head>
<body>
<h1>Autonomous SRE Demo</h1>
<p>Multi-agent self-healing ECS deployment</p>
<div class="card">
  <h2>Frontend</h2>
  <p class="ok">Healthy — Python Flask on ECS Fargate</p>
</div>
<div class="card">
  <h2>Backend API</h2>
  <div id="status">Checking...</div>
</div>
<script>
fetch("/api/backend-status")
  .then(r => r.json())
  .then(d => {
    document.getElementById("status").innerHTML =
      d.status === "healthy"
        ? '<span class="ok">Healthy — ' + d.service + '</span>'
        : '<span class="err">Error: ' + (d.error || d.status) + '</span>';
  })
  .catch(e => {
    document.getElementById("status").innerHTML =
      '<span class="err">Unreachable: ' + e.message + '</span>';
  });
</script>
</body>
</html>"""


@app.route("/")
def index():
    return HTML, 200, {"Content-Type": "text/html"}


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "frontend"}), 200


@app.route("/api/backend-status")
def backend_status():
    if not API_URL:
        return jsonify({"status": "unconfigured", "error": "BACKEND_API_URL not set"}), 503
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"status": "unreachable", "error": str(e)}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))