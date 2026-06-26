"""Tests del endpoint de reportes."""


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_monthly_report_responde_200(client):
    r = client.get("/reports/monthly")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


# TODO: re-activar cuando arreglemos el manejo de montos negativos
# def test_no_acepta_montos_negativos(client):
#     ...
