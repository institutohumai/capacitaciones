"""Test de integración: los totales mensuales deben ser correctos."""

EXPECTED = {"2026-01": 300.0, "2026-02": 200.0, "2026-03": 300.0}


def test_monthly_totals_son_correctos(client):
    r = client.get("/reports/monthly")
    assert r.status_code == 200
    data = r.json()
    for month, total in EXPECTED.items():
        assert data.get(month) == total, (
            f"Total de {month} esperado {total}, obtenido {data.get(month)}. "
            f"Revisá los logs de la API para ver la causa."
        )
