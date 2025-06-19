from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_weather_forecast():
    response = client.get("api/weather/forecast?latitude=50.0618&longitude=19.9368")
    assert response.status_code == 200
    data = response.json()
    for day in data:
        assert "date" in day
        assert "weather_code" in day
        assert "min_temp" in day
        assert "max_temp" in day
        assert "energy" in day or "estimated_energy_kwh" in day 

def test_get_weather_forecast_invalid_latitude():
    response = client.get("api/weather/forecast?latitude=100&longitude=19.9368")
    assert response.status_code == 400

def test_get_weather_forecast_invalid_longitude():
    response = client.get("api/weather/forecast?latitude=50.0618&longitude=200")
    assert response.status_code == 400

def test_get_week_summary():
    response = client.get("api/weather/summary?latitude=50.0618&longitude=19.9368")
    assert response.status_code == 200
    data = response.json()
    assert "average_pressure" in data
    assert "average_sun_exposure" in data
    assert "extreme_temperatures" in data
    assert "summary" in data

def test_get_week_summary_invalid_latitude():
    response = client.get("api/weather/summary?latitude=100&longitude=19.9368")
    assert response.status_code == 400

def test_get_week_summary_invalid_longitude():
    response = client.get("api/weather/summary?latitude=50.0618&longitude=200")
    assert response.status_code == 400