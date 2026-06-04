"use client";
import { useEffect, useState } from "react";

interface StatusData {
  status: string;
  message: string;
  timestamp: string;
  service: string;
}

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<StatusData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "/api";
    fetch(`${apiUrl}/status`)
      .then((r) => r.json())
      .then((data) => {
        setBackendStatus(data);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  return (
    <main style={{ fontFamily: "system-ui", padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>
        🤖 Autonomous SRE Demo
      </h1>
      <p style={{ color: "#666", marginBottom: "2rem" }}>
        Multi-agent self-healing ECS deployment · Frontend Service
      </p>

      <div style={{ display: "grid", gap: "1rem", gridTemplateColumns: "1fr 1fr" }}>
        <div style={{ padding: "1.5rem", border: "1px solid #e5e7eb", borderRadius: "8px" }}>
          <h2 style={{ fontSize: "1rem", color: "#374151", marginBottom: "0.5rem" }}>
            Frontend Status
          </h2>
          <span style={{ color: "#059669", fontWeight: "bold", fontSize: "1.2rem" }}>
            ✓ Healthy
          </span>
          <p style={{ color: "#6b7280", fontSize: "0.875rem", marginTop: "0.5rem" }}>
            Next.js running on ECS Fargate
          </p>
        </div>

        <div style={{ padding: "1.5rem", border: "1px solid #e5e7eb", borderRadius: "8px" }}>
          <h2 style={{ fontSize: "1rem", color: "#374151", marginBottom: "0.5rem" }}>
            Backend API Status
          </h2>
          {loading && <span style={{ color: "#6b7280" }}>Checking...</span>}
          {error && (
            <span style={{ color: "#dc2626", fontWeight: "bold" }}>
              ✗ {error}
            </span>
          )}
          {backendStatus && (
            <span style={{ color: "#059669", fontWeight: "bold", fontSize: "1.2rem" }}>
              ✓ {backendStatus.status}
            </span>
          )}
          {backendStatus && (
            <p style={{ color: "#6b7280", fontSize: "0.875rem", marginTop: "0.5rem" }}>
              {backendStatus.message}
            </p>
          )}
        </div>
      </div>

      <div style={{ marginTop: "2rem", padding: "1rem", background: "#f9fafb", borderRadius: "8px", fontSize: "0.875rem", color: "#6b7280" }}>
        <strong>Deployment info:</strong> This app is deployed via autonomous CI/CD.
        Each commit triggers dependency prediction, build, and self-healing stages.
      </div>
    </main>
  );
}
