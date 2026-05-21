def test_health_check_returns_operational_status(client):
    response = client.get("/api/v1/health", headers={"X-Request-ID": "test-health"})
    
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-health"
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "v1"
