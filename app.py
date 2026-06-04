from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

BACKEND_API_URL = os.environ.get("BACKEND_API_URL", "")

HTML = """<!DOCTYPE html>
<html>
<head>
<title>Autonomous SRE Demo</title>
<style>
body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 16px 0; }
.ok  { color: #059669; font-weight: bold; }
.err { color: #dc2626; font-weight: bold; }
pre  { background: #f4f4f4; padding: 10px; border-radius: 4px; font-size: 12px; }
</style>
</head>
<body>
<h1>Autonomous SRE Demo</h1>
<p>Multi-agent self-healing ECS deployment</p>

<div class="card">
  <h2>Frontend</h2>
  <p class="ok">&#10003; Healthy &mdash; Python Flask on ECS Fargate</p>
</div>

<div class="card">
  <h2>Backend API</h2>
  <div id="status">Checking...</div>
  <pre id="raw"></pre>
</div>

<script>
fetch("/api/backend-status")
  .then(r => {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  })
  .then(d => {
    document.getElementById("raw").textContent = JSON.stringify(d, null, 2);
    document.getElementById("status").innerHTML =
      d.status === "healthy"
        ? '<span class="ok">&#10003; Healthy &mdash; ' + (d.service || "backend") + '</span>'
        : '<span class="err">&#10007; ' + (d.error || d.status) + '</span>';
  })
  .catch(e => {
    document.getElementById("status").innerHTML =
      '<span class="err">&#10007; Fetch failed: ' + e.message + '</span>';
    document.getElementById("raw").textContent = "Check browser console for details";
  });
</script>
</body>
</html>"""


@app.route("/")
def index():
    return HTML, 200, {"Content-Type": "text/html; charset=utf-8"}


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "frontend"}), 200


@app.route("/api/backend-status")
def backend_status():
    if not BACKEND_API_URL:
        return jsonify({"status": "error", "error": "BACKEND_API_URL env var not set"}), 503
    try:
        # Try /health first, fall back to /api/status
        url = f"{BACKEND_API_URL}/health"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.exceptions.ConnectionError as e:
        return jsonify({"status": "unreachable", "error": f"Connection failed: {str(e)[:100]}"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"status": "unreachable", "error": "Timed out after 5s"}), 503
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)[:100]}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))