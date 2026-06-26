import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API}/reports/monthly`)
      .then((r) => r.json())
      .then(setData)
      .catch((e) => setError(String(e)));
  }, []);

  return (
    <main style={{ fontFamily: "Arial, sans-serif", maxWidth: 520, margin: "40px auto" }}>
      <h1>Reportes mensuales</h1>
      {error && <p data-testid="error">{error}</p>}
      {!data && !error && <p>Cargando…</p>}
      {data && (
        <table data-testid="reports-table" border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr><th>Mes</th><th>Total</th></tr>
          </thead>
          <tbody>
            {Object.entries(data).map(([month, total]) => (
              <tr key={month} data-testid={`row-${month}`}>
                <td>{month}</td>
                <td data-testid={`total-${month}`}>{total}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
